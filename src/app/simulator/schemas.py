from pydantic import BaseModel


class SimulationRequest(BaseModel):
    amount_usd: float
    days_history: int = 90


class DayAnalysis(BaseModel):
    wait_days: int
    avg_return: float
    std_dev: float
    worst_case: float
    best_case: float
    risk_zone: str


class SimulationResponse(BaseModel):
    daily_analysis: list[DayAnalysis]
    recommendation: str
    risk_level: str
    optimal_day: int
    expected_return: float
