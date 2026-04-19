from concurrent.futures import ThreadPoolExecutor
from ..services.mempool_client import MempoolClient

_mempool = MempoolClient()


def handle_network_status(body: dict) -> tuple[dict, int]:
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_fees = executor.submit(_mempool.get_recommended_fees)
        f_height = executor.submit(_mempool.get_block_tip_height)
        f_mempool = executor.submit(_mempool.get_mempool_info)

        try:
            fees = f_fees.result()
        except Exception:
            fees = {}

        try:
            block_height = f_height.result()
        except Exception:
            block_height = 0

        try:
            mempool_info = f_mempool.result()
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
