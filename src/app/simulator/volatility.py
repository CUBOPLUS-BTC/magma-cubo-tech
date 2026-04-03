import asyncio
import statistics
from ..services.coingecko_client import CoinGeckoClient
from .schemas import DayAnalysis, SimulationResponse


class VolatilitySimulator:
    def __init__(self):
        self.coingecko = CoinGeckoClient()

    async def simulate(self, amount_usd: float, days_history: int = 90) -> SimulationResponse:
        prices_data, btc_price = await asyncio.gather(
            self.coingecko.get_historical_prices(days=days_history),
            self.coingecko.get_price(),
            return_exceptions=True,
        )

        prices_data = prices_data if not isinstance(prices_data, Exception) else []
        btc_price = btc_price if not isinstance(btc_price, Exception) else 0.0

        prices = [entry[1] for entry in prices_data] if prices_data else []

        if len(prices) < 10:
            return SimulationResponse(
                daily_analysis=[],
                recommendation="Insufficient historical data to simulate",
                risk_level="unknown",
                optimal_day=0,
                expected_return=0.0,
            )

        daily_analysis: list[DayAnalysis] = []
        best_sharpe = float("-inf")
        optimal_day = 0
        optimal_return = 0.0

        for n in range(8):
            returns = []
            for i in range(len(prices) - n):
                if n == 0:
                    returns.append(0.0)
                else:
                    ret = (prices[i + n] - prices[i]) / prices[i] * 100
                    returns.append(ret)

            if not returns:
                continue

            avg_return = statistics.mean(returns)
            std_dev = statistics.stdev(returns) if len(returns) > 1 else 0.0
            worst_case = min(returns)
            best_case = max(returns)

            if std_dev < 2.0:
                risk_zone = "low"
            elif std_dev < 5.0:
                risk_zone = "medium"
            else:
                risk_zone = "high"

            sharpe = avg_return / std_dev if std_dev > 0 else 0.0

            if sharpe > best_sharpe and n > 0:
                best_sharpe = sharpe
                optimal_day = n
                optimal_return = avg_return

            daily_analysis.append(
                DayAnalysis(
                    wait_days=n,
                    avg_return=round(avg_return, 4),
                    std_dev=round(std_dev, 4),
                    worst_case=round(worst_case, 4),
                    best_case=round(best_case, 4),
                    risk_zone=risk_zone,
                )
            )

        optimal_analysis = next(
            (d for d in daily_analysis if d.wait_days == optimal_day), None
        )
        risk_level = optimal_analysis.risk_zone if optimal_analysis else "unknown"

        if optimal_return > 0:
            recommendation = (
                f"Wait {optimal_day} day(s) for an expected return of "
                f"{optimal_return:.2f}% (Sharpe: {best_sharpe:.2f})"
            )
        else:
            recommendation = (
                "Convert immediately — no waiting period shows a positive risk-adjusted return"
            )

        return SimulationResponse(
            daily_analysis=daily_analysis,
            recommendation=recommendation,
            risk_level=risk_level,
            optimal_day=optimal_day,
            expected_return=round(optimal_return, 4),
        )
