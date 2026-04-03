import httpx
import time
from typing import Optional, Any


class MempoolClient:
    def __init__(self, base_url: str = "https://mempool.space/api"):
        self.base_url = base_url
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

    async def get_address_info(self, address: str) -> dict:
        url = f"{self.base_url}/address/{address}"
        return await self._cached_get(f"addr_info_{address}", url, 300)

    async def get_address_txs(self, address: str) -> list:
        url = f"{self.base_url}/address/{address}/txs"
        return await self._cached_get(f"addr_txs_{address}", url, 300)

    async def get_address_utxos(self, address: str) -> list:
        url = f"{self.base_url}/address/{address}/utxo"
        return await self._cached_get(f"addr_utxos_{address}", url, 300)

    async def get_lightning_stats(self) -> dict:
        url = f"{self.base_url}/v1/lightning/statistics/latest"
        return await self._cached_get("ln_stats", url, 3600)

    async def get_recommended_fees(self) -> dict:
        url = f"{self.base_url}/v1/fees/recommended"
        return await self._cached_get("fees", url, 60)
