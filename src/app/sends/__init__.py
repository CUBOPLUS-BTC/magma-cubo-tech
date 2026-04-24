"""Sends module — resolve a Lightning address into a payable BOLT11 invoice.

Magma does not hold funds. This module only orchestrates the LNURL-pay
handshake so the user's wallet can sign and pay the resulting invoice.
"""

from .executor import SendExecutor

__all__ = ["SendExecutor"]
