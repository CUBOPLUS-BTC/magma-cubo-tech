"""CRUD + LNURL-pay validation for remittance recipients."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from ..database import _is_postgres, get_conn
from .schemas import (
    validate_amount,
    validate_country,
    validate_lightning_address,
    validate_name,
)


LNURL_PAY_TIMEOUT = 5  # seconds
USER_AGENT = "Magma/1.0 (+https://api.eclalune.com)"


class RecipientsManager:
    """Persists recipients and validates Lightning addresses on create."""

    # ------------------------------------------------------------------
    # LNURL-pay validation
    # ------------------------------------------------------------------

    def resolve_lnurl_pay(self, lightning_address: str) -> dict:
        """Fetch the LNURL-pay metadata for a Lightning address.

        Returns a dict with ``callback``, ``min_sendable_msat``,
        ``max_sendable_msat``. Raises ``ValueError`` on any failure so the
        caller can return 422 to the user with a readable message.
        """
        try:
            local, domain = lightning_address.split("@", 1)
        except ValueError:
            raise ValueError("Formato inválido")

        url = f"https://{domain}/.well-known/lnurlp/{urllib.parse.quote(local)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

        try:
            with urllib.request.urlopen(req, timeout=LNURL_PAY_TIMEOUT) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"El servidor de la wallet respondió {resp.status}"
                    )
                raw = resp.read(65536)
        except urllib.error.URLError as exc:
            raise ValueError(f"No se pudo contactar {domain}: {exc.reason}")
        except Exception as exc:
            raise ValueError(f"Fallo al resolver LNURL-pay: {exc}")

        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            raise ValueError("El servidor devolvió una respuesta inválida")

        if data.get("tag") != "payRequest":
            raise ValueError("El endpoint no soporta LNURL-pay")

        callback = data.get("callback")
        min_sendable = data.get("minSendable")
        max_sendable = data.get("maxSendable")

        if not callback or not isinstance(callback, str):
            raise ValueError("Metadata LNURL sin callback válido")
        try:
            min_sendable = int(min_sendable)
            max_sendable = int(max_sendable)
        except (TypeError, ValueError):
            raise ValueError("Metadata LNURL con rangos inválidos")

        return {
            "callback": callback,
            "min_sendable_msat": min_sendable,
            "max_sendable_msat": max_sendable,
        }

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(
        self,
        pubkey: str,
        name: str,
        lightning_address: str,
        country: str = "SV",
        default_amount_usd: Optional[float] = None,
        skip_lnurl_check: bool = False,
    ) -> dict:
        """Create a recipient for *pubkey*."""
        if not pubkey:
            raise ValueError("pubkey requerido")

        clean_name = validate_name(name)
        clean_address = validate_lightning_address(lightning_address)
        clean_country = validate_country(country)
        clean_amount = validate_amount(default_amount_usd)

        min_sendable_msat = None
        max_sendable_msat = None
        if not skip_lnurl_check:
            meta = self.resolve_lnurl_pay(clean_address)
            min_sendable_msat = meta["min_sendable_msat"]
            max_sendable_msat = meta["max_sendable_msat"]

        now = int(time.time())
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()

        if _is_postgres():
            cur = conn.cursor()
            cur.execute(
                f"""
                INSERT INTO recipients (
                    pubkey, name, lightning_address, country,
                    default_amount_usd, min_sendable_msat, max_sendable_msat,
                    created_at, updated_at
                ) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                RETURNING id
                """,
                (
                    pubkey, clean_name, clean_address, clean_country,
                    clean_amount, min_sendable_msat, max_sendable_msat,
                    now, now,
                ),
            )
            row = cur.fetchone()
            new_id = row[0] if not hasattr(row, "keys") else row["id"]
            conn.commit()
        else:
            cur = conn.execute(
                f"""
                INSERT INTO recipients (
                    pubkey, name, lightning_address, country,
                    default_amount_usd, min_sendable_msat, max_sendable_msat,
                    created_at, updated_at
                ) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                """,
                (
                    pubkey, clean_name, clean_address, clean_country,
                    clean_amount, min_sendable_msat, max_sendable_msat,
                    now, now,
                ),
            )
            new_id = cur.lastrowid
            conn.commit()

        return self.get(new_id, pubkey)

    def list_for_user(self, pubkey: str) -> list[dict]:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        rows = conn.execute(
            f"SELECT * FROM recipients WHERE pubkey = {ph} ORDER BY created_at DESC",
            (pubkey,),
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get(self, recipient_id: int, pubkey: str) -> dict:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        row = conn.execute(
            f"SELECT * FROM recipients WHERE id = {ph} AND pubkey = {ph}",
            (recipient_id, pubkey),
        ).fetchone()
        if row is None:
            raise KeyError(f"Recipient {recipient_id!r} no encontrado")
        return self._row_to_dict(row)

    def delete(self, recipient_id: int, pubkey: str) -> bool:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        cur = conn.execute(
            f"DELETE FROM recipients WHERE id = {ph} AND pubkey = {ph}",
            (recipient_id, pubkey),
        )
        conn.commit()
        return (cur.rowcount or 0) > 0

    def update(self, recipient_id: int, pubkey: str, updates: dict) -> dict:
        """Partial update. Allowed: name, country, default_amount_usd."""
        self.get(recipient_id, pubkey)  # raises KeyError if missing
        allowed = {"name", "country", "default_amount_usd"}
        fields = {k: v for k, v in updates.items() if k in allowed}
        if not fields:
            raise ValueError(
                f"Sin campos válidos. Permitidos: {sorted(allowed)}"
            )

        if "name" in fields:
            fields["name"] = validate_name(fields["name"])
        if "country" in fields:
            fields["country"] = validate_country(fields["country"])
        if "default_amount_usd" in fields:
            fields["default_amount_usd"] = validate_amount(fields["default_amount_usd"])

        ph = "%s" if _is_postgres() else "?"
        set_parts = [f"{k} = {ph}" for k in fields.keys()]
        set_parts.append(f"updated_at = {ph}")
        params = list(fields.values()) + [int(time.time()), recipient_id, pubkey]

        conn = get_conn()
        conn.execute(
            f"UPDATE recipients SET {', '.join(set_parts)} "
            f"WHERE id = {ph} AND pubkey = {ph}",
            params,
        )
        conn.commit()
        return self.get(recipient_id, pubkey)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row) -> dict:
        if row is None:
            return {}
        if hasattr(row, "keys"):
            return dict(row)
        cols = [
            "id", "pubkey", "name", "lightning_address", "country",
            "default_amount_usd", "min_sendable_msat", "max_sendable_msat",
            "created_at", "updated_at",
        ]
        return dict(zip(cols, row))
