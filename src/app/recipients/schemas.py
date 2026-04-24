"""Validation helpers for recipient payloads."""

from __future__ import annotations

import re

# Conservative lightning address validator: local-part@domain with TLD.
_LN_ADDRESS_RE = re.compile(
    r"^[a-z0-9][a-z0-9._\-]*[a-z0-9]@[a-z0-9][a-z0-9.\-]*\.[a-z]{2,}$",
    re.IGNORECASE,
)

ALLOWED_COUNTRIES = {
    "SV", "MX", "GT", "HN", "NI", "CR", "PA",
    "CO", "EC", "PE", "BO", "AR", "CL", "UY",
    "VE", "DO", "CU", "US", "CA", "ES",
}

MAX_NAME_LEN = 80


def validate_lightning_address(address: str) -> str:
    """Return the normalised address or raise ``ValueError``."""
    if not isinstance(address, str):
        raise ValueError("lightning_address debe ser string")
    clean = address.strip().lower()
    if not _LN_ADDRESS_RE.match(clean):
        raise ValueError(f"Lightning address inválida: {address!r}")
    return clean


def validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError("name debe ser string")
    clean = name.strip()
    if not clean:
        raise ValueError("name no puede estar vacío")
    if len(clean) > MAX_NAME_LEN:
        raise ValueError(f"name excede {MAX_NAME_LEN} caracteres")
    return clean


def validate_country(code: str) -> str:
    if not isinstance(code, str):
        raise ValueError("country debe ser string (ISO-3166 alpha-2)")
    clean = code.strip().upper()
    if clean not in ALLOWED_COUNTRIES:
        raise ValueError(f"country no soportado: {clean!r}")
    return clean


def validate_amount(amount) -> float | None:
    if amount is None:
        return None
    try:
        value = float(amount)
    except (TypeError, ValueError):
        raise ValueError("default_amount_usd debe ser numérico")
    if value <= 0:
        raise ValueError("default_amount_usd debe ser mayor a 0")
    if value > 100_000:
        raise ValueError("default_amount_usd excede el máximo permitido")
    return value
