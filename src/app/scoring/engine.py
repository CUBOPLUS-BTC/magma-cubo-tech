import asyncio
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

    async def calculate_score(self, address: str) -> ScoreResponse:
        address_info, txs, utxos, ln_stats = await asyncio.gather(
            self.mempool.get_address_info(address),
            self.mempool.get_address_txs(address),
            self.mempool.get_address_utxos(address),
            self.mempool.get_lightning_stats(),
            return_exceptions=True,
        )

        btc_price = await self.coingecko.get_price()

        address_info = address_info if not isinstance(address_info, Exception) else {}
        txs = txs if not isinstance(txs, Exception) else []
        utxos = utxos if not isinstance(utxos, Exception) else []
        ln_stats = ln_stats if not isinstance(ln_stats, Exception) else {}

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
                "relative_volume": {"score": breakdown["relative_volume"], "max": 150},
                "diversification": {"score": breakdown["diversification"], "max": 100},
                "savings_pattern": {"score": breakdown["savings_pattern"], "max": 150},
                "payment_history": {"score": breakdown["payment_history"], "max": 150},
                "lightning_activity": {
                    "score": breakdown["lightning_activity"],
                    "max": 100,
                },
            },
            recommendations=recommendations,
        )
