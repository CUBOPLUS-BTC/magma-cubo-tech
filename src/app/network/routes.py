from ..services.mempool_client import MempoolClient

_mempool = MempoolClient()


def handle_network_status(body: dict) -> tuple[dict, int]:
    try:
        fees = _mempool.get_recommended_fees()
    except Exception:
        fees = {}

    try:
        block_height = _mempool.get_block_tip_height()
    except Exception:
        block_height = 0

    try:
        mempool_info = _mempool.get_mempool_info()
    except Exception:
        mempool_info = {}

    return {
        "fees": fees,
        "block_height": block_height,
        "mempool_size": {
            "count": mempool_info.get("count", 0),
            "vsize": mempool_info.get("vsize", 0),
        },
    }, 200
