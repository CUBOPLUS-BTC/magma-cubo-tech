import re


def validate_pubkey(s: str) -> bool:
    """Validate hex pubkey is exactly 64 characters."""
    return bool(re.match(r"^[a-fA-F0-9]{64}$", s))


def validate_amount(n: float, min_val: float = 0, max_val: float = 1_000_000) -> bool:
    """Validate amount is within acceptable range."""
    return min_val <= n <= max_val


def validate_string(s: str, max_len: int = 256) -> bool:
    """Validate string is not empty and within length limit."""
    return bool(s and len(s) <= max_len)
