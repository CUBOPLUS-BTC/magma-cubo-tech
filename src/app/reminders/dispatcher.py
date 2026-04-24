"""Dispatcher — sends reminder payloads through configured channels.

Channels:
- ``webhook``  : uses the existing WebhookDispatcher and the
                 ``remittance_reminder`` event type. User must subscribe
                 to that event in /webhooks beforehand.
- ``nostr_dm`` : publishes a NIP-04 encrypted DM. Requires a Nostr
                 keypair on the server side. If unavailable, the channel
                 logs a warning and records status='skipped'.
- ``email``    : posts to Resend if ``RESEND_API_KEY`` is configured.
                 Otherwise records status='skipped'.

The dispatcher is intentionally tolerant: a failure in one channel never
stops the others. Each delivery attempt is written to
``reminder_events`` via the manager so the user can inspect history.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Optional

from ..config import settings
from ..database import _is_postgres, get_conn
from .manager import RemindersManager


class ReminderDispatcher:
    """Fan-out delivery of a reminder across its configured channels."""

    def __init__(
        self,
        manager: RemindersManager,
        webhook_dispatcher=None,
    ) -> None:
        self.manager = manager
        self.webhook_dispatcher = webhook_dispatcher

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def dispatch(self, reminder: dict) -> dict:
        """Dispatch a single reminder. Returns summary dict per channel."""
        reminder_id = reminder["id"]
        pubkey = reminder["pubkey"]
        channels = reminder.get("channels") or []

        payload = self._build_payload(reminder)
        results: dict[str, dict] = {}

        for channel in channels:
            try:
                if channel == "webhook":
                    status, error = self._deliver_webhook(pubkey, payload)
                elif channel == "nostr_dm":
                    status, error = self._deliver_nostr(pubkey, payload)
                elif channel == "email":
                    status, error = self._deliver_email(pubkey, payload)
                else:
                    status, error = "skipped", f"unknown channel {channel!r}"
            except Exception as exc:  # defensive: a bug must not break others
                status, error = "failed", f"{type(exc).__name__}: {exc}"

            self.manager.record_event(reminder_id, channel, status, error)
            results[channel] = {"status": status, "error": error}

        self.manager.mark_fired(reminder_id, int(time.time()))
        return {"reminder_id": reminder_id, "channels": results}

    # ------------------------------------------------------------------
    # Payload builder
    # ------------------------------------------------------------------

    def _build_payload(self, reminder: dict) -> dict:
        recipient = self._load_recipient(reminder["recipient_id"])
        amount = recipient.get("default_amount_usd")
        return {
            "event": "remittance_reminder",
            "reminder_id": reminder["id"],
            "recipient": {
                "id": recipient.get("id"),
                "name": recipient.get("name"),
                "lightning_address": recipient.get("lightning_address"),
                "country": recipient.get("country"),
            },
            "amount_usd": amount,
            "cadence": reminder.get("cadence"),
            "fired_at": int(time.time()),
            "message_es": self._render_message_es(recipient, amount),
            "message_en": self._render_message_en(recipient, amount),
        }

    @staticmethod
    def _render_message_es(recipient: dict, amount: Optional[float]) -> str:
        name = recipient.get("name", "tu destinatario")
        if amount:
            return (
                f"Hora de enviar tu remesa mensual a {name} "
                f"(${amount:,.0f} USD). Abrí Magma para ver la ruta más barata hoy."
            )
        return (
            f"Hora de enviar tu remesa mensual a {name}. "
            "Abrí Magma para ver la ruta más barata hoy."
        )

    @staticmethod
    def _render_message_en(recipient: dict, amount: Optional[float]) -> str:
        name = recipient.get("name", "your recipient")
        if amount:
            return (
                f"Time to send your monthly remittance to {name} "
                f"(${amount:,.0f} USD). Open Magma to see today's cheapest route."
            )
        return (
            f"Time to send your monthly remittance to {name}. "
            "Open Magma to see today's cheapest route."
        )

    @staticmethod
    def _load_recipient(recipient_id: int) -> dict:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        row = conn.execute(
            f"SELECT * FROM recipients WHERE id = {ph}", (recipient_id,)
        ).fetchone()
        if row is None:
            return {"id": recipient_id}
        if hasattr(row, "keys"):
            return dict(row)
        cols = [
            "id", "pubkey", "name", "lightning_address", "country",
            "default_amount_usd", "min_sendable_msat", "max_sendable_msat",
            "created_at", "updated_at",
        ]
        return dict(zip(cols, row))

    # ------------------------------------------------------------------
    # Channel delivery
    # ------------------------------------------------------------------

    def _deliver_webhook(self, pubkey: str, payload: dict) -> tuple[str, Optional[str]]:
        if self.webhook_dispatcher is None:
            return "skipped", "webhook dispatcher no configurado"
        try:
            self.webhook_dispatcher.dispatch(
                "remittance_reminder", payload, pubkeys=[pubkey]
            )
            return "sent", None
        except Exception as exc:
            return "failed", f"{type(exc).__name__}: {exc}"

    def _deliver_nostr(self, pubkey: str, payload: dict) -> tuple[str, Optional[str]]:
        """Publish NIP-04 DM. This is a stub — real implementation lives in
        ``app.nostr`` and can be wired up once the server-side signing key
        is provisioned. For the hackathon we return ``skipped`` rather than
        failing the reminder entirely.
        """
        try:
            from ..nostr import publish_encrypted_dm  # type: ignore
        except Exception:
            return "skipped", "nostr DM helper no disponible"

        try:
            publish_encrypted_dm(
                recipient_pubkey=pubkey,
                content=payload["message_es"],
                metadata=payload,
            )
            return "sent", None
        except Exception as exc:
            return "failed", f"{type(exc).__name__}: {exc}"

    def _deliver_email(self, pubkey: str, payload: dict) -> tuple[str, Optional[str]]:
        api_key = os.environ.get("RESEND_API_KEY") or getattr(
            settings, "RESEND_API_KEY", ""
        )
        if not api_key:
            return "skipped", "RESEND_API_KEY no configurado"

        # We don't store user emails yet; they must be added to user_preferences
        # in a future migration. For now, skip gracefully.
        email = self._lookup_user_email(pubkey)
        if not email:
            return "skipped", "usuario sin email registrado"

        from_addr = os.environ.get("RESEND_FROM") or getattr(
            settings, "RESEND_FROM", "notify@eclalune.com"
        )
        body = {
            "from": from_addr,
            "to": [email],
            "subject": "Hora de tu remesa mensual en Magma",
            "text": payload["message_es"],
        }
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Magma/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status >= 300:
                    return "failed", f"resend status {resp.status}"
                return "sent", None
        except urllib.error.URLError as exc:
            return "failed", f"resend error: {exc.reason}"
        except Exception as exc:
            return "failed", f"{type(exc).__name__}: {exc}"

    @staticmethod
    def _lookup_user_email(pubkey: str) -> Optional[str]:
        """Best-effort email lookup. Returns None if column does not exist.

        A future migration will add ``email`` to ``user_preferences``; until
        then we probe the column and return ``None`` if it is missing so the
        reminder system keeps working.
        """
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        try:
            row = conn.execute(
                f"SELECT email FROM user_preferences WHERE pubkey = {ph}",
                (pubkey,),
            ).fetchone()
        except Exception:
            return None
        if row is None:
            return None
        if hasattr(row, "keys"):
            return row["email"]  # type: ignore[index]
        return row[0]
