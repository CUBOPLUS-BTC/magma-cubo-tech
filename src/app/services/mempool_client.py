import urllib.request
import urllib.error
import json
import time
from typing import Any


class MempoolClient:
    _shared_cache: dict[str, tuple[Any, float]] = {}

    PRIMARY_URL = "https://mempool.space/api"
    FALLBACK_URL = "https://blockstream.info/api"

    def __init__(self, base_url: str = PRIMARY_URL):
        self.base_url = base_url

    def _fetch(self, url: str) -> Any:
        req = urllib.request.Request(url, headers={"User-Agent": "Magma/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())

    def _cached_get(self, key: str, url: str, ttl: int) -> Any:
        now = time.time()
        if key in self._shared_cache:
            data, expiry = self._shared_cache[key]
            if now < expiry:
                return data
        data = self._fetch(url)
        self._shared_cache[key] = (data, now + ttl)
        return data

    def _cached_get_with_fallback(self, key: str, primary_url: str, fallback_url: str, ttl: int) -> Any:
        now = time.time()
        if key in self._shared_cache:
            data, expiry = self._shared_cache[key]
            if now < expiry:
                return data
        try:
            data = self._fetch(primary_url)
        except Exception:
            data = self._fetch(fallback_url)
        self._shared_cache[key] = (data, now + ttl)
        return data

    def get_recommended_fees(self) -> dict:
        # Intenta mempool.space primero, cae en blockstream si falla
        try:
            data = self._cached_get("fees", f"{self.PRIMARY_URL}/v1/fees/recommended", 60)
            if isinstance(data, dict) and "fastestFee" in data:
                return data
        except Exception:
            pass

        # Blockstream devuelve {block_target: sat/vB} — lo mapeamos al schema de mempool.space
        try:
            raw = self._cached_get("fees_bs", f"{self.FALLBACK_URL}/fee-estimates", 60)
            fast = raw.get("2", raw.get("3", 1))
            half = raw.get("6", raw.get("9", 1))
            economy = raw.get("144", raw.get("24", 1))
            return {
                "fastestFee": round(fast),
                "halfHourFee": round(half),
                "hourFee": round(half),
                "economyFee": round(economy),
                "minimumFee": 1,
            }
        except Exception:
            return {}

    def get_block_tip_height(self) -> int:
        try:
            return int(self._cached_get_with_fallback(
                "block_height",
                f"{self.PRIMARY_URL}/blocks/tip/height",
                f"{self.FALLBACK_URL}/blocks/tip/height",
                60,
            ))
        except Exception:
            return 0

    def get_mempool_info(self) -> dict:
        try:
            return self._cached_get("mempool_info", f"{self.PRIMARY_URL}/mempool", 60)
        except Exception:
            # blockstream no tiene endpoint de mempool equivalente
            return {"count": 0, "vsize": 0}

    def get_address_info(self, address: str) -> dict:
        return self._cached_get_with_fallback(
            f"addr_info_{address}",
            f"{self.PRIMARY_URL}/address/{address}",
            f"{self.FALLBACK_URL}/address/{address}",
            300,
        )

    def get_address_txs(self, address: str) -> list:
        return self._cached_get_with_fallback(
            f"addr_txs_{address}",
            f"{self.PRIMARY_URL}/address/{address}/txs",
            f"{self.FALLBACK_URL}/address/{address}/txs",
            300,
        )

    def get_address_utxos(self, address: str) -> list:
        return self._cached_get_with_fallback(
            f"addr_utxos_{address}",
            f"{self.PRIMARY_URL}/address/{address}/utxo",
            f"{self.FALLBACK_URL}/address/{address}/utxo",
            300,
        )

    def get_lightning_stats(self) -> dict:
        try:
            return self._cached_get("ln_stats", f"{self.PRIMARY_URL}/v1/lightning/statistics/latest", 3600)
        except Exception:
            return {}
