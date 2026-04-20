"""Alerts feed and monitor status."""

from __future__ import annotations

from typing import List

from ..models import Alert
from ._base import Resource


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
