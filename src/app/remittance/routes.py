from .optimizer import RemittanceOptimizer
from .fees import FeeTracker

_optimizer = RemittanceOptimizer()
_fee_tracker = FeeTracker()


def handle_compare(body: dict) -> tuple[dict, int]:
    """POST /remittance/compare"""
    try:
        amount_usd = float(body.get("amount_usd", 0))
        frequency = body.get("frequency", "monthly")
        result = _optimizer.compare(amount_usd=amount_usd, frequency=frequency)
        return result.to_dict(), 200
    except Exception as e:
        return {"detail": str(e)}, 500


def handle_fees(body: dict) -> tuple[dict, int]:
    """GET /remittance/fees"""
    try:
        current_fees = _fee_tracker.get_current_fees()
        best_time = _fee_tracker.get_best_send_time()
        return {"fees": current_fees, "best_time": best_time}, 200
    except Exception as e:
        return {"detail": str(e)}, 500
