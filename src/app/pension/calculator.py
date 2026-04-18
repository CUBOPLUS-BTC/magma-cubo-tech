from ..services.coingecko_client import CoinGeckoClient
from .schemas import PensionProjection


class PensionCalculator:
    def __init__(self):
        self.coingecko = CoinGeckoClient()

    def project(self, monthly_saving_usd: float, years: int) -> PensionProjection:
        total_months = years * 12

        # Get current price
        try:
            current_price = self.coingecko.get_price()
        except Exception:
            current_price = 0.0

        # Get historical prices (max available from CoinGecko free: ~365 days)
        try:
            historical = self.coingecko.get_historical_prices(days=365)
        except Exception:
            historical = []

        # Build monthly average prices from historical data
        monthly_prices = self._extract_monthly_prices(historical)

        # If we don't have enough historical months, fill with average
        if monthly_prices:
            avg_historical = sum(monthly_prices) / len(monthly_prices)
        else:
            avg_historical = current_price if current_price > 0 else 60000.0

        while len(monthly_prices) < total_months:
            monthly_prices.append(avg_historical)

        # Simulate DCA
        total_invested = 0.0
        total_btc = 0.0
        breakdown = []

        for month_idx in range(total_months):
            price = monthly_prices[month_idx]
            if price <= 0:
                price = avg_historical

            btc_bought = monthly_saving_usd / price
            total_invested += monthly_saving_usd
            total_btc += btc_bought

            value_at_current = total_btc * current_price if current_price > 0 else 0.0

            breakdown.append(
                {
                    "month": month_idx + 1,
                    "invested": round(total_invested, 2),
                    "btc_bought": round(btc_bought, 8),
                    "btc_total": round(total_btc, 8),
                    "value_usd": round(value_at_current, 2),
                }
            )

        avg_buy_price = (total_invested / total_btc) if total_btc > 0 else 0.0
        current_value = total_btc * current_price if current_price > 0 else 0.0

        monthly_data = []
        for m in range(1, years * 12 + 1):
            month_usd = monthly_saving_usd * m
            btc_at_month = (monthly_saving_usd / avg_historical) * m
            btc_value = btc_at_month * current_price
            monthly_data.append(
                {
                    "month": m,
                    "invested": round(month_usd, 2),
                    "traditional_value": round(month_usd * (1.02 ** (m / 12)), 2),
                    "btc_value": round(btc_value, 2),
                }
            )

        return PensionProjection(
            total_invested_usd=round(total_invested, 2),
            total_btc_accumulated=round(total_btc, 8),
            current_value_usd=round(current_value, 2),
            avg_buy_price=round(avg_buy_price, 2),
            current_btc_price=round(current_price, 2),
            monthly_breakdown=breakdown,
            monthly_data=monthly_data,
        )

    def _extract_monthly_prices(self, historical: list) -> list[float]:
        """Extract one price per month from daily historical data."""
        if not historical:
            return []

        monthly: list[float] = []
        current_month = None

        for timestamp_ms, price in historical:
            # Convert ms timestamp to month key
            import time

            t = time.gmtime(timestamp_ms / 1000)
            month_key = (t.tm_year, t.tm_mon)

            if month_key != current_month:
                monthly.append(price)
                current_month = month_key

        return monthly
