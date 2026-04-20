"""Public price endpoint."""

from __future__ import annotations

from ..models import PriceQuote
from ._base import Resource


class PriceResource(Resource):
    def get(self) -> PriceQuote:
        """Return the verified BTC price."""
        data = self._get("/price")
        return PriceQuote.from_dict(data if isinstance(data, dict) else {})
