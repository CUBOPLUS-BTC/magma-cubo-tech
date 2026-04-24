"""LNURL-pay executor — converts (recipient, amount_usd) into a BOLT11 invoice.

Flow
----
1. Look up the recipient (owned by the authenticated user).
2. Get the current verified BTC price from the aggregator.
3. Convert ``amount_usd`` to millisats.
4. Call the LNURL-pay callback stored for the recipient (or re-resolve if
   missing) with ``amount=<msat>``.
5. Return the ``pr`` (BOLT11 invoice) plus a ``lightning:`` deeplink the
   frontend opens to hand off to the user's wallet.

We never store invoices or payment results — that is the wallet's job.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from ..recipients.manager import RecipientsManager, USER_AGENT

LNURL_CALLBACK_TIMEOUT = 8  # seconds


class SendExecutor:
    """Orchestrate LNURL-pay callback for a stored recipient."""

    def __init__(
        self,
        recipients_manager: RecipientsManager,
        price_aggregator,
    ) -> None:
        self.recipients = recipients_manager
        self.price_agg = price_aggregator

    def build_invoice(
        self,
        recipient_id: int,
        pubkey: str,
        amount_usd: float,
        comment: Optional[str] = None,
    ) -> dict:
        """Return ``{bolt11, deeplink, amount_sats, amount_msat, recipient}``.

        Raises ``ValueError`` on any validation or network failure so the
        route handler can translate to 4xx.
        """
        if amount_usd is None or amount_usd <= 0:
            raise ValueError("amount_usd debe ser mayor a 0")
        if amount_usd > 100_000:
            raise ValueError("amount_usd excede el máximo permitido")

        recipient = self.recipients.get(recipient_id, pubkey)

        price = self._current_btc_price()
        if price <= 0:
            raise ValueError("Precio BTC no disponible en este momento")

        btc_amount = float(amount_usd) / price
        amount_sats = int(round(btc_amount * 100_000_000))
        amount_msat = amount_sats * 1000

        min_msat = recipient.get("min_sendable_msat")
        max_msat = recipient.get("max_sendable_msat")
        if min_msat and amount_msat < int(min_msat):
            raise ValueError(
                f"Monto bajo el mínimo permitido por la wallet receptora "
                f"({int(min_msat) // 1000} sats)"
            )
        if max_msat and amount_msat > int(max_msat):
            raise ValueError(
                f"Monto sobre el máximo permitido por la wallet receptora "
                f"({int(max_msat) // 1000} sats)"
            )

        callback = self._resolve_callback(recipient)
        invoice = self._call_callback(callback, amount_msat, comment)

        bolt11 = invoice.get("pr")
        if not bolt11 or not isinstance(bolt11, str):
            raise ValueError("La wallet receptora no devolvió un invoice válido")

        return {
            "bolt11": bolt11,
            "deeplink": f"lightning:{bolt11}",
            "amount_usd": round(float(amount_usd), 2),
            "amount_sats": amount_sats,
            "amount_msat": amount_msat,
            "btc_price_usd": round(price, 2),
            "recipient": {
                "id": recipient["id"],
                "name": recipient["name"],
                "lightning_address": recipient["lightning_address"],
                "country": recipient.get("country"),
            },
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _current_btc_price(self) -> float:
        try:
            data = self.price_agg.get_verified_price()
            return float(data.get("price_usd") or 0)
        except Exception:
            try:
                return float(self.price_agg.get_current_price("BTC") or 0)
            except Exception:
                return 0.0

    def _resolve_callback(self, recipient: dict) -> str:
        """Fetch LNURL-pay metadata to obtain the callback URL.

        We do not persist callbacks because some wallets rotate them.
        Re-resolving every send is cheap (one HTTPS request).
        """
        meta = self.recipients.resolve_lnurl_pay(recipient["lightning_address"])
        return meta["callback"]

    @staticmethod
    def _call_callback(
        callback: str,
        amount_msat: int,
        comment: Optional[str],
    ) -> dict:
        """Call the LNURL-pay callback and return the parsed JSON."""
        params = {"amount": str(amount_msat)}
        if comment:
            params["comment"] = comment[:144]

        sep = "&" if "?" in callback else "?"
        url = f"{callback}{sep}{urllib.parse.urlencode(params)}"

        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=LNURL_CALLBACK_TIMEOUT) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"LNURL callback respondió {resp.status}"
                    )
                raw = resp.read(65536)
        except urllib.error.URLError as exc:
            raise ValueError(f"No se pudo contactar la wallet receptora: {exc.reason}")
        except Exception as exc:
            raise ValueError(f"Fallo LNURL callback: {exc}")

        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            raise ValueError("La wallet receptora devolvió JSON inválido")

        if data.get("status") == "ERROR":
            reason = data.get("reason") or "desconocido"
            raise ValueError(f"Wallet receptora rechazó el pago: {reason}")

        return data
