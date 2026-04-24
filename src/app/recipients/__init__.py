"""Remittance recipients module.

Manages the list of recipients (family members, beneficiaries) that a user
sends remittances to. Validates Lightning addresses on creation by pinging
the LNURL-pay endpoint.
"""

from .manager import RecipientsManager

__all__ = ["RecipientsManager"]
