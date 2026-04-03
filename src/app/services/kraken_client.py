import httpx
import time
from typing import Any


class KrakenClient:
    def __init__(self):
        self.base_url = "https://api.kraken.com/0/public"
        self._cache: dict[str, tuple[Any, float]] = {}

    async def _cached_get(self, key: str, url: str, ttl: int) -> Any:
        now = time.time()
        if key in self._cache:
            data, expiry = self._cache[key]
            if now < expiry:
                return data

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        self._cache[key] = (data, now + ttl)
        return data

    async def get_price(self) -> float:
        url = f"{self.base_url}/Ticker?pair=XXBTZUSD"
        data = await self._cached_get("kraken_price", url, 60)
        return float(data["result"]["XXBTZUSD"]["c"][0])
