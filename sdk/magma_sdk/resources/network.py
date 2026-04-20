"""Bitcoin network status."""

from __future__ import annotations

from ._base import Resource


class NetworkResource(Resource):
    def status(self) -> dict:
        """GET /network/status — block height, lightning stats, etc."""
        return self._get("/network/status")
