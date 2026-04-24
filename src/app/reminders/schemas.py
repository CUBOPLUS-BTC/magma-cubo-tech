"""Validation + scheduling helpers for reminders."""

from __future__ import annotations

import datetime as _dt
from typing import Iterable

ALLOWED_CADENCES = {"monthly", "biweekly", "custom"}
ALLOWED_CHANNELS = {"webhook", "nostr_dm", "email"}

DEFAULT_TIMEZONE = "America/El_Salvador"


def validate_cadence(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("cadence debe ser string")
    clean = value.strip().lower()
    if clean not in ALLOWED_CADENCES:
        raise ValueError(
            f"cadence inválida: {clean!r}. Permitidos: {sorted(ALLOWED_CADENCES)}"
        )
    return clean


def validate_day_of_month(value) -> int:
    try:
        day = int(value)
    except (TypeError, ValueError):
        raise ValueError("day_of_month debe ser entero")
    if not (1 <= day <= 28):
        raise ValueError("day_of_month debe estar entre 1 y 28")
    return day


def validate_hour(value) -> int:
    try:
        hour = int(value)
    except (TypeError, ValueError):
        raise ValueError("hour_local debe ser entero")
    if not (0 <= hour <= 23):
        raise ValueError("hour_local debe estar entre 0 y 23")
    return hour


def validate_channels(value: Iterable) -> list[str]:
    if not isinstance(value, (list, tuple, set)):
        raise ValueError("channels debe ser lista")
    clean = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError("channels debe contener strings")
        name = item.strip().lower()
        if name not in ALLOWED_CHANNELS:
            raise ValueError(
                f"channel inválido: {name!r}. Permitidos: {sorted(ALLOWED_CHANNELS)}"
            )
        if name not in clean:
            clean.append(name)
    if not clean:
        raise ValueError("Se requiere al menos un channel")
    return clean


def validate_timezone(value: str) -> str:
    """Best-effort timezone validation without zoneinfo dependency.

    We only enforce it is a string; the dispatcher falls back to UTC offset
    calculations when zoneinfo is unavailable on the host.
    """
    if not isinstance(value, str):
        raise ValueError("timezone debe ser string")
    clean = value.strip()
    if not clean:
        return DEFAULT_TIMEZONE
    return clean


def compute_next_fire_at(
    cadence: str,
    day_of_month: int,
    hour_local: int,
    timezone: str,
    reference_utc_ts: int | None = None,
) -> int:
    """Compute the next fire timestamp (epoch UTC) for a reminder.

    The algorithm is intentionally simple — we treat ``hour_local`` as an
    hour in the reminder's timezone, convert to UTC using ``zoneinfo`` when
    available, and fall back to treating it as UTC otherwise.
    """
    try:
        from zoneinfo import ZoneInfo  # type: ignore[import-not-found]
        tz = ZoneInfo(timezone)
    except Exception:
        tz = _dt.timezone.utc

    if reference_utc_ts is None:
        now = _dt.datetime.now(tz=_dt.timezone.utc).astimezone(tz)
    else:
        now = _dt.datetime.fromtimestamp(reference_utc_ts, tz=_dt.timezone.utc).astimezone(tz)

    def _build(year: int, month: int) -> _dt.datetime:
        # Clamp day_of_month to last day of month just in case.
        try:
            return _dt.datetime(year, month, day_of_month, hour_local, 0, 0, tzinfo=tz)
        except ValueError:
            # Month has fewer days than day_of_month — step back one day at a time.
            day = day_of_month
            while day > 0:
                try:
                    return _dt.datetime(year, month, day, hour_local, 0, 0, tzinfo=tz)
                except ValueError:
                    day -= 1
            raise

    candidate = _build(now.year, now.month)
    if candidate <= now:
        # Move to next period.
        if cadence == "biweekly":
            candidate = candidate + _dt.timedelta(days=14)
        else:  # monthly / custom default
            if now.month == 12:
                candidate = _build(now.year + 1, 1)
            else:
                candidate = _build(now.year, now.month + 1)

    return int(candidate.astimezone(_dt.timezone.utc).timestamp())
