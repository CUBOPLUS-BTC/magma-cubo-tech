"""CRUD for reminders. Reads/writes the ``reminders`` + ``reminder_events`` tables."""

from __future__ import annotations

import json
import time
from typing import Optional

from ..database import _is_postgres, get_conn
from .schemas import (
    DEFAULT_TIMEZONE,
    compute_next_fire_at,
    validate_cadence,
    validate_channels,
    validate_day_of_month,
    validate_hour,
    validate_timezone,
)


class RemindersManager:
    """Persist and query remittance reminders."""

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(
        self,
        pubkey: str,
        recipient_id: int,
        cadence: str = "monthly",
        day_of_month: int = 1,
        hour_local: int = 9,
        timezone: str = DEFAULT_TIMEZONE,
        channels: Optional[list[str]] = None,
    ) -> dict:
        if not pubkey:
            raise ValueError("pubkey requerido")
        if not isinstance(recipient_id, int) or recipient_id <= 0:
            raise ValueError("recipient_id inválido")

        # Verify recipient belongs to this user.
        self._assert_recipient_owned(recipient_id, pubkey)

        clean_cadence = validate_cadence(cadence)
        clean_day = validate_day_of_month(day_of_month)
        clean_hour = validate_hour(hour_local)
        clean_tz = validate_timezone(timezone)
        clean_channels = validate_channels(channels or ["webhook"])

        now = int(time.time())
        next_fire = compute_next_fire_at(
            clean_cadence, clean_day, clean_hour, clean_tz, reference_utc_ts=now
        )

        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        params = (
            pubkey, recipient_id, clean_cadence, clean_day, clean_hour, clean_tz,
            json.dumps(clean_channels), 0, next_fire, None, 0, now, now,
        )

        if _is_postgres():
            cur = conn.cursor()
            cur.execute(
                f"""
                INSERT INTO reminders (
                    pubkey, recipient_id, cadence, day_of_month, hour_local,
                    timezone, channels, paused, next_fire_at, last_fired_at,
                    fire_count, created_at, updated_at
                ) VALUES ({', '.join([ph] * 13)})
                RETURNING id
                """,
                params,
            )
            row = cur.fetchone()
            new_id = row[0] if not hasattr(row, "keys") else row["id"]
            conn.commit()
        else:
            cur = conn.execute(
                f"""
                INSERT INTO reminders (
                    pubkey, recipient_id, cadence, day_of_month, hour_local,
                    timezone, channels, paused, next_fire_at, last_fired_at,
                    fire_count, created_at, updated_at
                ) VALUES ({', '.join([ph] * 13)})
                """,
                params,
            )
            new_id = cur.lastrowid
            conn.commit()

        return self.get(new_id, pubkey)

    def list_for_user(self, pubkey: str) -> list[dict]:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        rows = conn.execute(
            f"SELECT * FROM reminders WHERE pubkey = {ph} ORDER BY created_at DESC",
            (pubkey,),
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get(self, reminder_id: int, pubkey: str) -> dict:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        row = conn.execute(
            f"SELECT * FROM reminders WHERE id = {ph} AND pubkey = {ph}",
            (reminder_id, pubkey),
        ).fetchone()
        if row is None:
            raise KeyError(f"Reminder {reminder_id!r} no encontrado")
        return self._row_to_dict(row)

    def update(self, reminder_id: int, pubkey: str, updates: dict) -> dict:
        current = self.get(reminder_id, pubkey)
        allowed = {"cadence", "day_of_month", "hour_local", "timezone", "channels", "paused"}
        fields = {k: v for k, v in updates.items() if k in allowed}
        if not fields:
            raise ValueError(f"Sin campos válidos. Permitidos: {sorted(allowed)}")

        if "cadence" in fields:
            fields["cadence"] = validate_cadence(fields["cadence"])
        if "day_of_month" in fields:
            fields["day_of_month"] = validate_day_of_month(fields["day_of_month"])
        if "hour_local" in fields:
            fields["hour_local"] = validate_hour(fields["hour_local"])
        if "timezone" in fields:
            fields["timezone"] = validate_timezone(fields["timezone"])
        if "channels" in fields:
            fields["channels"] = json.dumps(validate_channels(fields["channels"]))
        if "paused" in fields:
            fields["paused"] = 1 if fields["paused"] else 0

        # Recompute next_fire_at when any schedule-related field changes.
        schedule_changed = any(
            k in fields for k in ("cadence", "day_of_month", "hour_local", "timezone")
        )
        if schedule_changed or (fields.get("paused") == 0 and current.get("paused")):
            fields["next_fire_at"] = compute_next_fire_at(
                fields.get("cadence", current["cadence"]),
                fields.get("day_of_month", current["day_of_month"]),
                fields.get("hour_local", current["hour_local"]),
                fields.get("timezone", current["timezone"]),
            )

        ph = "%s" if _is_postgres() else "?"
        set_parts = [f"{k} = {ph}" for k in fields.keys()]
        set_parts.append(f"updated_at = {ph}")
        params = list(fields.values()) + [int(time.time()), reminder_id, pubkey]

        conn = get_conn()
        conn.execute(
            f"UPDATE reminders SET {', '.join(set_parts)} "
            f"WHERE id = {ph} AND pubkey = {ph}",
            params,
        )
        conn.commit()
        return self.get(reminder_id, pubkey)

    def delete(self, reminder_id: int, pubkey: str) -> bool:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        cur = conn.execute(
            f"DELETE FROM reminders WHERE id = {ph} AND pubkey = {ph}",
            (reminder_id, pubkey),
        )
        conn.commit()
        return (cur.rowcount or 0) > 0

    # ------------------------------------------------------------------
    # Scheduler helpers (no user context)
    # ------------------------------------------------------------------

    def due_reminders(self, now_ts: int) -> list[dict]:
        """Return non-paused reminders whose ``next_fire_at`` <= now_ts."""
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        rows = conn.execute(
            f"SELECT * FROM reminders "
            f"WHERE paused = 0 AND next_fire_at <= {ph}",
            (now_ts,),
        ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def mark_fired(self, reminder_id: int, fired_at: int) -> None:
        """Advance next_fire_at, bump fire_count, set last_fired_at."""
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        # Re-read current state to compute next fire correctly.
        row = conn.execute(
            f"SELECT * FROM reminders WHERE id = {ph}", (reminder_id,)
        ).fetchone()
        if row is None:
            return
        rec = self._row_to_dict(row)
        next_fire = compute_next_fire_at(
            rec["cadence"], rec["day_of_month"], rec["hour_local"],
            rec["timezone"], reference_utc_ts=fired_at + 60,
        )
        conn.execute(
            f"""
            UPDATE reminders
            SET last_fired_at = {ph},
                next_fire_at  = {ph},
                fire_count    = fire_count + 1,
                updated_at    = {ph}
            WHERE id = {ph}
            """,
            (fired_at, next_fire, int(time.time()), reminder_id),
        )
        conn.commit()

    def record_event(
        self,
        reminder_id: int,
        channel: str,
        status: str,
        error: Optional[str] = None,
    ) -> None:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        conn.execute(
            f"""
            INSERT INTO reminder_events (reminder_id, channel, status, error, fired_at)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
            """,
            (reminder_id, channel, status, error, int(time.time())),
        )
        conn.commit()

    def list_events(self, reminder_id: int, pubkey: str, limit: int = 50) -> list[dict]:
        self.get(reminder_id, pubkey)  # ownership check
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        rows = conn.execute(
            f"""
            SELECT id, reminder_id, channel, status, error, fired_at
            FROM reminder_events
            WHERE reminder_id = {ph}
            ORDER BY fired_at DESC
            LIMIT {ph}
            """,
            (reminder_id, int(limit)),
        ).fetchall()
        return [self._event_row_to_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _assert_recipient_owned(recipient_id: int, pubkey: str) -> None:
        ph = "%s" if _is_postgres() else "?"
        conn = get_conn()
        row = conn.execute(
            f"SELECT id FROM recipients WHERE id = {ph} AND pubkey = {ph}",
            (recipient_id, pubkey),
        ).fetchone()
        if row is None:
            raise KeyError(f"Recipient {recipient_id!r} no pertenece al usuario")

    @staticmethod
    def _row_to_dict(row) -> dict:
        if row is None:
            return {}
        if hasattr(row, "keys"):
            d = dict(row)
        else:
            cols = [
                "id", "pubkey", "recipient_id", "cadence", "day_of_month",
                "hour_local", "timezone", "channels", "paused",
                "next_fire_at", "last_fired_at", "fire_count",
                "created_at", "updated_at",
            ]
            d = dict(zip(cols, row))

        channels_raw = d.get("channels", "[]")
        if isinstance(channels_raw, str):
            try:
                d["channels"] = json.loads(channels_raw)
            except json.JSONDecodeError:
                d["channels"] = []
        d["paused"] = bool(d.get("paused", 0))
        return d

    @staticmethod
    def _event_row_to_dict(row) -> dict:
        if row is None:
            return {}
        if hasattr(row, "keys"):
            return dict(row)
        cols = ["id", "reminder_id", "channel", "status", "error", "fired_at"]
        return dict(zip(cols, row))
