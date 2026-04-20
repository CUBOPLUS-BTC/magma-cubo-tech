"""Pension projection endpoint."""

from __future__ import annotations

import math

from ..exceptions import MagmaError
from ..models import PensionProjection
from ._base import Resource


class PensionResource(Resource):
    def project(
        self, monthly_saving_usd: float, years: int
    ) -> PensionProjection:
        """POST /pension/projection — 20+ year DCA projection (public)."""
        if (
            not isinstance(monthly_saving_usd, (int, float))
            or isinstance(monthly_saving_usd, bool)
            or not math.isfinite(monthly_saving_usd)
            or monthly_saving_usd <= 0
        ):
            raise MagmaError("monthly_saving_usd must be a positive finite number")
        if not isinstance(years, int) or isinstance(years, bool) or years < 1:
            raise MagmaError("years must be a positive integer")

        data = self._post(
            "/pension/projection",
            json_body={
                "monthly_saving_usd": monthly_saving_usd,
                "years": years,
            },
        )
        return PensionProjection.from_dict(data if isinstance(data, dict) else {})
