from datetime import datetime, timezone
from ..services.mempool_client import MempoolClient


class FeeTracker:
    def __init__(self):
        self.mempool = MempoolClient()

    async def get_current_fees(self) -> dict:
        return await self.mempool.get_recommended_fees()

    async def get_best_send_time(self) -> dict:
        fees = await self.mempool.get_recommended_fees()

        current_fee = fees.get("halfHourFee", 10) if isinstance(fees, dict) else 10
        economy_fee = fees.get("economyFee", 5) if isinstance(fees, dict) else 5

        estimated_low = min(economy_fee, int(current_fee * 0.6))
        estimated_low = max(estimated_low, 1)

        now = datetime.now(timezone.utc)
        is_weekend = now.weekday() >= 5
        is_low_hour = 2 <= now.hour <= 6

        if is_weekend and is_low_hour:
            best_time = "Now — current time is in the optimal window (weekend 2-6 AM UTC)"
        elif is_weekend:
            best_time = "Today between 2-6 AM UTC (weekend low-fee window)"
        else:
            best_time = "Next Saturday or Sunday, 2-6 AM UTC"

        return {
            "best_time": best_time,
            "current_fee_sat_vb": current_fee,
            "estimated_low_fee_sat_vb": estimated_low,
        }
