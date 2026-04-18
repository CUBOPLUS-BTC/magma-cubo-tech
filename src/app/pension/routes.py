from .calculator import PensionCalculator

_calculator = PensionCalculator()


def handle_projection(body: dict) -> tuple[dict, int]:
    monthly = body.get("monthly_saving_usd", 0)
    years = body.get("years", 0)

    if not monthly or monthly <= 0:
        return {"detail": "monthly_saving_usd must be positive"}, 400
    if not years or years <= 0 or years > 50:
        return {"detail": "years must be between 1 and 50"}, 400

    try:
        projection = _calculator.project(float(monthly), int(years))
        return projection.to_dict(), 200
    except Exception as e:
        return {"detail": str(e)}, 500
