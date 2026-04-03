import httpx
import time
from typing import Optional, Any


class CoinGeckoClient:
    def __init__(self, api_key: str = ""):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.api_key = api_key
        self._cache: dict[str, tuple[Any, float]] = {}

    def _headers(self) -> dict:
        if self.api_key:
            return {"x-cg-demo-api-key": self.api_key}
        return {}

    async def _cached_get(self, key: str, url: str, ttl: int) -> Any:
        now = time.time()
        if key in self._cache:
            data, expiry = self._cache[key]
            if now < expiry:
                return data

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self._headers())
            response.raise_for_status()
            data = response.json()

        self._cache[key] = (data, now + ttl)
        return data

    async def get_price(self) -> float:
        url = f"{self.base_url}/simple/price?ids=bitcoin&vs_currencies=usd"
        data = await self._cached_get("btc_price", url, 60)
        return float(data["bitcoin"]["usd"])

    async def get_historical_prices(self, days: int = 90) -> list:
        """Get historical BTC prices from CoinGecko market_chart endpoint.

        Returns a list of [timestamp_ms, price_usd] entries.
        Cached for 1 hour (3600s) since historical data changes infrequently.
        """
        url = (
            f"{self.base_url}/coins/bitcoin/market_chart"
            f"?vs_currency=usd&days={days}"
        )
        data = await self._cached_get(f"historical_{days}", url, 3600)
        return data.get("prices", [])
