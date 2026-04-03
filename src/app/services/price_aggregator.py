import asyncio
from typing import Optional
from .mempool_client import MempoolClient
from .coingecko_client import CoinGeckoClient
from .kraken_client import KrakenClient


class PriceUnavailableError(Exception):
    pass


class PriceAggregator:
    def __init__(self, coingecko_key: str = ""):
        self.mempool = MempoolClient()
        self.coingecko = CoinGeckoClient(coingecko_key)
        self.kraken = KrakenClient()

    async def get_verified_price(self) -> dict:
        results = await asyncio.gather(
            self._get_mempool_price(),
            self._get_coingecko_price(),
            self._get_kraken_price(),
            return_exceptions=True,
        )

        prices = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue
            prices.append(result)

        if len(prices) == 0:
            raise PriceUnavailableError("No price sources available")

        median_price = sorted(prices)[len(prices) // 2]

        deviation = 0.0
        if len(prices) >= 2:
            max_deviation = max(abs(p - median_price) / median_price for p in prices)
            deviation = round(max_deviation * 100, 2)

        return {
            "price_usd": round(median_price, 2),
            "sources_count": len(prices),
            "deviation": deviation,
            "has_warning": len(prices) < 2,
        }

    async def _get_mempool_price(self) -> float:
        fees = await self.mempool.get_recommended_fees()
        return float(fees.get("today", 0))

    async def _get_coingecko_price(self) -> float:
        return await self.coingecko.get_price()

    async def _get_kraken_price(self) -> float:
        return await self.kraken.get_price()
