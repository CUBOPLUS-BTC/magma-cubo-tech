from concurrent.futures import ThreadPoolExecutor
from ..services.mempool_client import MempoolClient
from ..services.coingecko_client import CoinGeckoClient
from .onchain import (
    calculate_consistency,
    calculate_volume,
    calculate_savings,
    calculate_payment_history,
)
from .lightning import calculate_layer_diversity, calculate_lightning_activity
from .schemas import ScoreResponse, classify_rank, generate_recommendations


class ScoringEngine:
    def __init__(self):
        self.mempool = MempoolClient()
        self.coingecko = CoinGeckoClient()

    def calculate_score(self, address: str) -> ScoreResponse:
        with ThreadPoolExecutor(max_workers=4) as executor:
            f_info = executor.submit(self.mempool.get_address_info, address)
            f_txs = executor.submit(self.mempool.get_address_txs, address)
            f_utxos = executor.submit(self.mempool.get_address_utxos, address)
            f_ln = executor.submit(self.mempool.get_lightning_stats)

            try:
                address_info = f_info.result()
            except Exception:
                address_info = {}
            try:
                txs = f_txs.result()
            except Exception:
                txs = []
            try:
                utxos = f_utxos.result()
            except Exception:
                utxos = []
            try:
                ln_stats = f_ln.result()
            except Exception:
                ln_stats = {}

        try:
            btc_price = self.coingecko.get_price()
        except Exception:
            btc_price = 0.0

        breakdown = {
            "consistency": calculate_consistency(txs),
            "relative_volume": calculate_volume(address_info, btc_price),
            "diversification": calculate_layer_diversity(len(txs), ln_stats),
            "savings_pattern": calculate_savings(address_info, utxos),
            "payment_history": calculate_payment_history(txs),
            "lightning_activity": calculate_lightning_activity(ln_stats),
        }

        total_score = sum(breakdown.values())
        rank = classify_rank(total_score)
        recommendations = generate_recommendations(breakdown)

        return ScoreResponse(
            total_score=total_score,
            rank=rank,
            address=address,
            breakdown={
                "consistency": {"score": breakdown["consistency"], "max": 200},
                "relative_volume": {
                    "score": breakdown["relative_volume"],
                    "max": 150,
                },
                "diversification": {
                    "score": breakdown["diversification"],
                    "max": 100,
                },
                "savings_pattern": {
                    "score": breakdown["savings_pattern"],
                    "max": 150,
                },
                "payment_history": {
                    "score": breakdown["payment_history"],
                    "max": 150,
                },
                "lightning_activity": {
                    "score": breakdown["lightning_activity"],
                    "max": 100,
                },
            },
            recommendations=recommendations,
        )
