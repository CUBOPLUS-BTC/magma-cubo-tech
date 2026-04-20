"""Webhook signing and verification primitives.

Magma signs outbound webhook deliveries with HMAC-SHA256 over the raw
request body, using a shared secret shared out-of-band with each
integrator. Two headers travel with every delivery:

* ``X-Magma-Signature`` — hex-encoded HMAC digest.
* ``X-Magma-Timestamp`` — Unix seconds at which the signature was
  computed. Used to reject replays.

The functions here let both sides of the conversation (the backend
that sends the webhook, and the consumer that receives it) speak the
same dialect.

Example — receiving end::

    from magma_sdk.webhooks import WebhookVerifier, WebhookError

    verifier = WebhookVerifier(secret="shhh")

    try:
        event = verifier.verify(
            body=request.body,
            signature=request.headers["X-Magma-Signature"],
            timestamp=request.headers["X-Magma-Timestamp"],
        )
    except WebhookError:
        return 400
    handle(event)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional, Union


SIGNATURE_HEADER = "X-Magma-Signature"
TIMESTAMP_HEADER = "X-Magma-Timestamp"

DEFAULT_TOLERANCE_SECONDS = 300  # 5 minutes either side of "now"


class WebhookError(Exception):
    """Base class for webhook verification failures."""


class InvalidSignatureError(WebhookError):
    """The provided signature did not match the expected HMAC."""


class ReplayError(WebhookError):
    """The timestamp is outside the accepted tolerance window."""


class MalformedWebhookError(WebhookError):
    """The headers / body could not be parsed."""


def _to_bytes(value: Union[bytes, bytearray, memoryview, str]) -> bytes:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    raise MalformedWebhookError("payload must be bytes or str")


def _signed_payload(timestamp: str, body: bytes) -> bytes:
    return f"{timestamp}.".encode("utf-8") + body


def sign(
    body: Union[bytes, str],
    secret: Union[bytes, str],
    *,
    timestamp: Optional[int] = None,
    now: Optional[int] = None,
) -> dict[str, str]:
    """Produce the headers a sender should attach to a webhook delivery."""
    if not secret:
        raise MalformedWebhookError("secret is required")
    secret_bytes = _to_bytes(secret)
    if not secret_bytes:
        raise MalformedWebhookError("secret is required")

    ts = timestamp if timestamp is not None else (now if now is not None else int(time.time()))
    ts_str = str(int(ts))
    payload = _signed_payload(ts_str, _to_bytes(body))
    digest = hmac.new(secret_bytes, payload, hashlib.sha256).hexdigest()

    return {
        SIGNATURE_HEADER: digest,
        TIMESTAMP_HEADER: ts_str,
    }


@dataclass(frozen=True)
class WebhookEvent:
    """Parsed and verified webhook payload."""

    type: str
    data: dict
    timestamp: int
    raw: dict = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: dict, timestamp: int) -> "WebhookEvent":
        if not isinstance(payload, dict):
            raise MalformedWebhookError("webhook body must be a JSON object")
        return cls(
            type=str(payload.get("type", "")),
            data=payload.get("data", {}) if isinstance(payload.get("data"), dict) else {},
            timestamp=int(timestamp),
            raw=payload,
        )


class WebhookVerifier:
    """Stateless verifier for Magma-signed webhook deliveries."""

    def __init__(
        self,
        secret: Union[bytes, str],
        *,
        tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
    ) -> None:
        if not secret:
            raise MalformedWebhookError("secret is required")
        if tolerance_seconds < 0:
            raise MalformedWebhookError("tolerance_seconds must be >= 0")
        self._secret = _to_bytes(secret)
        self._tolerance = tolerance_seconds

    def expected_signature(
        self, body: Union[bytes, str], timestamp: Union[int, str]
    ) -> str:
        """Return the hex digest that should accompany ``body``."""
        ts_str = str(int(timestamp))
        payload = _signed_payload(ts_str, _to_bytes(body))
        return hmac.new(self._secret, payload, hashlib.sha256).hexdigest()

    def verify(
        self,
        body: Union[bytes, str],
        signature: str,
        timestamp: Union[int, str],
        *,
        now: Optional[int] = None,
        parse: bool = True,
    ) -> WebhookEvent:
        """Verify ``body`` + ``signature`` and, if valid, return the event.

        Raises :class:`InvalidSignatureError` on mismatch or
        :class:`ReplayError` when the timestamp is outside the tolerance
        window. Set ``parse=False`` to skip JSON parsing and just validate.
        """
        if not isinstance(signature, str) or not signature:
            raise InvalidSignatureError("signature is required")
        try:
            ts_int = int(timestamp)
        except (TypeError, ValueError) as exc:
            raise ReplayError("timestamp must be an integer") from exc

        current = int(now) if now is not None else int(time.time())
        if self._tolerance and abs(current - ts_int) > self._tolerance:
            raise ReplayError(
                f"timestamp {ts_int} outside tolerance of {self._tolerance}s"
            )

        expected = self.expected_signature(body, ts_int)
        if not hmac.compare_digest(expected, signature.strip().lower()):
            raise InvalidSignatureError("signature mismatch")

        if not parse:
            return WebhookEvent(type="", data={}, timestamp=ts_int, raw={})

        body_bytes = _to_bytes(body)
        try:
            payload: Any = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except json.JSONDecodeError as exc:
            raise MalformedWebhookError("body is not valid JSON") from exc
        if not isinstance(payload, dict):
            raise MalformedWebhookError("body must decode to a JSON object")
        return WebhookEvent.from_payload(payload, ts_int)

    def verify_request(
        self,
        body: Union[bytes, str],
        headers: "dict[str, str] | Any",
        *,
        now: Optional[int] = None,
    ) -> WebhookEvent:
        """Convenience that pulls signature + timestamp from ``headers``.

        Accepts a ``dict`` or any mapping whose keys are case-insensitive
        (e.g., ``email.message.Message``, ``werkzeug.datastructures.Headers``).
        """
        sig = _header_lookup(headers, SIGNATURE_HEADER)
        ts = _header_lookup(headers, TIMESTAMP_HEADER)
        if not sig or not ts:
            raise MalformedWebhookError("missing signature or timestamp header")
        return self.verify(body=body, signature=sig, timestamp=ts, now=now)


def _header_lookup(headers: Any, name: str) -> Optional[str]:
    if headers is None:
        return None
    # Dict-like case-insensitive lookup.
    try:
        for k, v in headers.items():
            if str(k).lower() == name.lower():
                return str(v)
    except AttributeError:
        return None
    return None
