import asyncio
import statistics
from ..services.coingecko_client import CoinGeckoClient


class ConversionStrategy:
    def __init__(self):
        self.coingecko = CoinGeckoClient()

    async def recommend(self, amount_usd: float, days_history: int = 90) -> dict:
        prices_data, btc_price = await asyncio.gather(
            self.coingecko.get_historical_prices(days=days_history),
            self.coingecko.get_price(),
            return_exceptions=True,
        )

        prices_data = prices_data if not isinstance(prices_data, Exception) else []
        btc_price = btc_price if not isinstance(btc_price, Exception) else 0.0

        prices = [entry[1] for entry in prices_data] if prices_data else []

        if len(prices) < 10 or btc_price <= 0:
            return {
                "strategy": "lump_sum",
                "explanation": "Insufficient data — defaulting to lump sum",
                "lump_sum": {"amount_btc": 0.0, "risk_level": "unknown"},
                "dca": {"amount_btc": 0.0, "risk_level": "unknown"},
            }

        lump_sum_btc = amount_usd / btc_price

        dca_intervals = 4
        interval_amount = amount_usd / dca_intervals
        dca_prices = []

        step = max(1, len(prices) // dca_intervals)
        for i in range(dca_intervals):
            idx = min(i * step, len(prices) - 1)
            dca_prices.append(prices[idx])

        dca_btc = sum(interval_amount / p for p in dca_prices if p > 0)

        daily_returns = [
            (prices[i + 1] - prices[i]) / prices[i] * 100
            for i in range(len(prices) - 1)
        ]
        volatility = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0.0

        lump_sharpe = (lump_sum_btc / (amount_usd / btc_price) - 1) / max(volatility, 0.01)
        dca_volatility = volatility / (dca_intervals ** 0.5)
        dca_sharpe = (dca_btc / (amount_usd / btc_price) - 1) / max(dca_volatility, 0.01)

        if volatility < 2.0:
            lump_risk = "low"
            dca_risk = "low"
        elif volatility < 5.0:
            lump_risk = "medium"
            dca_risk = "low"
        else:
            lump_risk = "high"
            dca_risk = "medium"

        if volatility > 3.0:
            strategy = "dca"
            explanation = (
                f"High volatility ({volatility:.1f}% daily std dev) detected. "
                f"DCA over 4 weeks reduces risk exposure."
            )
        else:
            strategy = "lump_sum"
            explanation = (
                f"Low volatility ({volatility:.1f}% daily std dev) detected. "
                f"Lump sum conversion is efficient."
            )

        return {
            "strategy": strategy,
            "explanation": explanation,
            "lump_sum": {
                "amount_btc": round(lump_sum_btc, 8),
                "risk_level": lump_risk,
                "sharpe_ratio": round(lump_sharpe, 4),
            },
            "dca": {
                "amount_btc": round(dca_btc, 8),
                "num_purchases": dca_intervals,
                "risk_level": dca_risk,
                "sharpe_ratio": round(dca_sharpe, 4),
            },
        }
