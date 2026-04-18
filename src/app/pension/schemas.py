from dataclasses import dataclass, field


@dataclass
class PensionRequest:
    monthly_saving_usd: float
    years: int


@dataclass
class PensionProjection:
    total_invested_usd: float
    total_btc_accumulated: float
    current_value_usd: float
    avg_buy_price: float
    current_btc_price: float
    monthly_breakdown: list = field(default_factory=list)
    monthly_data: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_invested_usd": self.total_invested_usd,
            "total_btc_accumulated": self.total_btc_accumulated,
            "current_value_usd": self.current_value_usd,
            "avg_buy_price": self.avg_buy_price,
            "current_btc_price": self.current_btc_price,
            "monthly_breakdown": self.monthly_breakdown,
            "monthly_data": self.monthly_data,
        }
