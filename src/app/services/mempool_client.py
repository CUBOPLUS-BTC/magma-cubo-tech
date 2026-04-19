import urllib.request
import urllib.error
import json
import time
from typing import Any


class MempoolClient:
    # Shared cache across all instances to avoid duplicate API calls
    _shared_cache: dict[str, tuple[Any, float]] = {}

    def __init__(self, base_url: str = "https://mempool.space/api"):
        self.base_url = base_url

    def _cached_get(self, key: str, url: str, ttl: int) -> Any:
        now = time.time()
        if key in self._shared_cache:
            data, expiry = self._shared_cache[key]
            if now < expiry:
                return data

        req = urllib.request.Request(url, headers={"User-Agent": "Magma/1.0"})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())

        self._shared_cache[key] = (data, now + ttl)
        return data

    def get_address_info(self, address: str) -> dict:
        url = f"{self.base_url}/address/{address}"
        return self._cached_get(f"addr_info_{address}", url, 300)

    def get_address_txs(self, address: str) -> list:
        url = f"{self.base_url}/address/{address}/txs"
        return self._cached_get(f"addr_txs_{address}", url, 300)

    def get_address_utxos(self, address: str) -> list:
        url = f"{self.base_url}/address/{address}/utxo"
        return self._cached_get(f"addr_utxos_{address}", url, 300)

    def get_lightning_stats(self) -> dict:
        url = f"{self.base_url}/v1/lightning/statistics/latest"
        return self._cached_get("ln_stats", url, 3600)

    def get_recommended_fees(self) -> dict:
        url = f"{self.base_url}/v1/fees/recommended"
        return self._cached_get("fees", url, 60)

    def get_block_tip_height(self) -> int:
        url = f"{self.base_url}/blocks/tip/height"
        return int(self._cached_get("block_height", url, 60))

    def get_mempool_info(self) -> dict:
        url = f"{self.base_url}/mempool"
        return self._cached_get("mempool_info", url, 60)
