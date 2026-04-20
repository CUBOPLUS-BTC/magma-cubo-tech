"""Alerts feed and monitor status."""

from __future__ import annotations

import time
from typing import Callable, Iterator, List, Optional

from ..models import Alert
from ._base import Resource


def _alert_key(alert: Alert) -> tuple:
    """Stable dedup key for an alert without a guaranteed id."""
    return (alert.created_at, alert.type, alert.message)


class AlertsResource(Resource):
    def list(self, limit: int = 20) -> List[Alert]:
        """GET /alerts — recent alerts (most recent first)."""
        if not isinstance(limit, int) or limit <= 0:
            limit = 20
        data = self._get("/alerts", query={"limit": limit})
        raw_alerts = (
            data.get("alerts", []) if isinstance(data, dict) else []
        )
        return [Alert.from_dict(a) for a in raw_alerts if isinstance(a, dict)]

    def status(self) -> dict:
        """GET /alerts/status — monitor health check."""
        return self._get("/alerts/status")

    def iter_new(
        self,
        *,
        since: Optional[int] = None,
        poll_interval: float = 5.0,
        limit: int = 50,
        max_iterations: Optional[int] = None,
        stop: Optional[Callable[[], bool]] = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> Iterator[Alert]:
        """Yield alerts newer than ``since`` by polling ``/alerts``.

        The iterator never terminates on its own; break out of the loop,
        provide ``max_iterations`` (useful in tests), or pass a ``stop``
        predicate returning ``True`` when the caller is done.

        Transport failures are surfaced so the caller can decide whether
        to retry or shut down — use a ``try/except`` around ``next()``.
        """
        if poll_interval < 0:
            raise ValueError("poll_interval must be >= 0")

        cursor = since
        seen: set[tuple] = set()
        iteration = 0

        while True:
            iteration += 1
            alerts = self.list(limit=limit)
            # Oldest first so callers observe them in chronological order.
            alerts.sort(key=lambda a: (a.created_at or 0))

            for alert in alerts:
                ts = alert.created_at
                key = _alert_key(alert)
                if cursor is not None and ts is not None and ts <= cursor:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                yield alert
                if ts is not None:
                    cursor = ts if cursor is None else max(cursor, ts)

            if stop is not None and stop():
                return
            if max_iterations is not None and iteration >= max_iterations:
                return
            if poll_interval > 0:
                sleep(poll_interval)
