"""Remittance comparison endpoints."""

from __future__ import annotations

import math

from ..exceptions import MagmaError
from ..models import RemittanceComparison
from ._base import Resource


_VALID_FREQUENCIES = frozenset({"monthly", "biweekly", "weekly"})


class RemittanceResource(Resource):
    def compare(
        self, amount_usd: float, frequency: str = "monthly"
    ) -> RemittanceComparison:
        """POST /remittance/compare — compare channels for ``amount_usd``."""
        if (
            not isinstance(amount_usd, (int, float))
            or isinstance(amount_usd, bool)
            or not math.isfinite(amount_usd)
            or amount_usd <= 0
        ):
            raise MagmaError("amount_usd must be a positive finite number")
        if frequency not in _VALID_FREQUENCIES:
            raise MagmaError(
                f"frequency must be one of {sorted(_VALID_FREQUENCIES)}"
            )

        data = self._post(
            "/remittance/compare",
            json_body={"amount_usd": amount_usd, "frequency": frequency},
        )
        return RemittanceComparison.from_dict(data if isinstance(data, dict) else {})

    def fees(self) -> dict:
        """GET /remittance/fees — current on-chain fee snapshot."""
        return self._get("/remittance/fees")
