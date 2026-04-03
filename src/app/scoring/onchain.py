from typing import List
import statistics


def calculate_consistency(txs: list) -> int:
    if not txs:
        return 0

    timestamps = []
    for tx in txs:
        if isinstance(tx, dict) and "status" in tx and "block_time" in tx["status"]:
            timestamps.append(tx["status"]["block_time"])

    if len(timestamps) < 2:
        return 50

    sorted_times = sorted(timestamps)
    intervals = [
        sorted_times[i + 1] - sorted_times[i] for i in range(len(sorted_times) - 1)
    ]

    if not intervals:
        return 50

    mean_interval = statistics.mean(intervals)
    if mean_interval == 0:
        return 50

    std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0
    cv = std_interval / mean_interval if mean_interval > 0 else 0

    score = int(200 * max(0, 1 - cv / 2.0))

    recent_time = max(timestamps)
    import time

    if time.time() - recent_time < 30 * 24 * 3600:
        score = min(score + 20, 200)

    return score


def calculate_volume(address_info: dict, btc_price: float) -> int:
    if not address_info:
        return 0

    funded_sum = address_info.get("funded_txo_sum", 0)
    total_usd = (funded_sum / 100_000_000) * btc_price

    reference_usd = 5000
    score = int(150 * min(total_usd / reference_usd, 1.0))

    return score


def calculate_savings(address_info: dict, utxos: list) -> int:
    if not address_info:
        return 0

    funded_sum = address_info.get("funded_txo_sum", 0)
    if funded_sum == 0:
        return 0

    balance = sum(utxo.get("value", 0) for utxo in utxos)
    ratio = balance / funded_sum

    score = int(150 * min(ratio * 2, 1.0))

    return score


def calculate_payment_history(txs: list) -> int:
    if not txs:
        return 0

    tx_count = len(txs)

    freq_score = min(tx_count / 50, 1.0) * 90

    timestamps = []
    for tx in txs:
        if isinstance(tx, dict) and "status" in tx and "block_time" in tx["status"]:
            timestamps.append(tx["status"]["block_time"])

    longevity_score = 0
    if len(timestamps) >= 2:
        min_time = min(timestamps)
        max_time = max(timestamps)
        months_active = (max_time - min_time) / (30 * 24 * 3600)
        longevity_score = min(months_active / 24, 1.0) * 60

    score = int(freq_score + longevity_score)

    return min(score, 150)
