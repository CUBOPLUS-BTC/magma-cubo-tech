"""Savings projection and tracking endpoints."""

from __future__ import annotations

import math
from typing import Optional

from ..exceptions import MagmaError
from ..models import SavingsProgress, SavingsProjection
from ._base import Resource


def _validate_monthly(monthly_usd: float) -> None:
    if not isinstance(monthly_usd, (int, float)) or isinstance(monthly_usd, bool):
        raise MagmaError("monthly_usd must be a number")
    if not math.isfinite(monthly_usd):
        raise MagmaError("monthly_usd must be finite")
    if monthly_usd <= 0:
        raise MagmaError("monthly_usd must be positive")


def _validate_years(years: int) -> None:
    if not isinstance(years, int) or isinstance(years, bool):
        raise MagmaError("years must be an integer")
    if years < 1 or years > 50:
        raise MagmaError("years must be between 1 and 50")


class SavingsResource(Resource):
    def project(self, monthly_usd: float, years: int = 10) -> SavingsProjection:
        """POST /savings/project — run a DCA projection (public)."""
        _validate_monthly(monthly_usd)
        _validate_years(years)
        data = self._post(
            "/savings/project",
            json_body={"monthly_usd": monthly_usd, "years": years},
        )
        return SavingsProjection.from_dict(data if isinstance(data, dict) else {})

    def create_goal(
        self,
        monthly_target_usd: float,
        target_years: int = 10,
        *,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        """POST /savings/goal — create or update the user's savings goal.

        Pass ``idempotency_key`` to make the request safe to retry; servers
        that honour the ``Idempotency-Key`` header will collapse duplicate
        submissions.
        """
        _validate_monthly(monthly_target_usd)
        _validate_years(target_years)
        return self._post(
            "/savings/goal",
            json_body={
                "monthly_target_usd": monthly_target_usd,
                "target_years": target_years,
            },
            auth=True,
            idempotency_key=idempotency_key,
        )

    def record_deposit(
        self, amount_usd: float, *, idempotency_key: Optional[str] = None
    ) -> dict:
        """POST /savings/deposit — record a new deposit.

        Pass ``idempotency_key`` (any unique string) to deduplicate retried
        writes. A UUID4 per user-level deposit is a good default.
        """
        if not isinstance(amount_usd, (int, float)) or isinstance(amount_usd, bool):
            raise MagmaError("amount_usd must be a number")
        if not math.isfinite(amount_usd):
            raise MagmaError("amount_usd must be finite")
        if amount_usd <= 0:
            raise MagmaError("amount_usd must be positive")
        return self._post(
            "/savings/deposit",
            json_body={"amount_usd": amount_usd},
            auth=True,
            idempotency_key=idempotency_key,
        )

    def progress(self) -> SavingsProgress:
        """GET /savings/progress — read current progress for the user."""
        data = self._get("/savings/progress", auth=True)
        return SavingsProgress.from_dict(data if isinstance(data, dict) else {})
