from dataclasses import dataclass


@dataclass
class SimulationRequest:
    amount_usd: float
    days_history: int = 90


@dataclass
class DayAnalysis:
    wait_days: int
    avg_return: float
    std_dev: float
    worst_case: float
    best_case: float
    risk_zone: str

    def to_dict(self) -> dict:
        return {
            "wait_days": self.wait_days,
            "avg_return": self.avg_return,
            "std_dev": self.std_dev,
            "worst_case": self.worst_case,
            "best_case": self.best_case,
            "risk_zone": self.risk_zone,
        }


@dataclass
class SimulationResponse:
    daily_analysis: list
    recommendation: str
    risk_level: str
    optimal_day: int
    expected_return: float

    def to_dict(self) -> dict:
        return {
            "daily_analysis": [
                d.to_dict() if hasattr(d, "to_dict") else d for d in self.daily_analysis
            ],
            "recommendation": self.recommendation,
            "risk_level": self.risk_level,
            "optimal_day": self.optimal_day,
            "expected_return": self.expected_return,
        }
