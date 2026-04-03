def calculate_layer_diversity(tx_count: int, ln_stats: dict) -> int:
    score = 0

    if tx_count > 0:
        score += 50

    if ln_stats and ln_stats.get("latest", {}).get("channel_count", 0) > 0:
        score += 50
    else:
        score += 25

    return min(score, 100)


def calculate_lightning_activity(ln_stats: dict) -> int:
    if not ln_stats:
        return 50

    channel_count = ln_stats.get("latest", {}).get("channel_count", 0)

    if channel_count > 100:
        return 100
    elif channel_count > 50:
        return 80
    else:
        return 50
