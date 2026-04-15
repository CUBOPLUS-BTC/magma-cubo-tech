from .volatility import VolatilitySimulator
from .conversion import ConversionStrategy

_simulator = VolatilitySimulator()
_conversion = ConversionStrategy()


def handle_volatility(body: dict) -> tuple[dict, int]:
    """POST /simulate/volatility"""
    try:
        amount_usd = float(body.get("amount_usd", 0))
        days_history = int(body.get("days_history", 90))
        result = _simulator.simulate(amount_usd=amount_usd, days_history=days_history)
        return result.to_dict(), 200
    except Exception as e:
        return {"detail": str(e)}, 500


def handle_conversion(body: dict) -> tuple[dict, int]:
    """POST /simulate/conversion"""
    try:
        amount_usd = float(body.get("amount_usd", 0))
        days_history = int(body.get("days_history", 90))
        result = _conversion.recommend(amount_usd=amount_usd, days_history=days_history)
        return result, 200
    except Exception as e:
        return {"detail": str(e)}, 500
