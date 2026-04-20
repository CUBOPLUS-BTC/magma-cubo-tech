"""Helpers consumers can use to test code that depends on the SDK.

Two building blocks:

* :class:`MockTransport` — drop-in for ``HTTPTransport`` that returns
  queued or route-matched responses without touching the network.
* :func:`make_test_client` — convenience factory returning a
  :class:`MagmaClient` wired to a fresh :class:`MockTransport`.

Consumers keep their production code paths intact and swap the client
at the edges:

    from magma_sdk.testing import MockTransport, make_test_client

    transport = MockTransport()
    transport.on("GET", "/price", {"price_usd": 50000})
    client = make_test_client(transport=transport)

    assert my_function(client).price == 50000
    assert transport.calls[0].path == "/price"
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, List, Optional

from ._transport import HTTPTransport
from .client import MagmaClient


@dataclass
class RecordedCall:
    method: str
    path: str
    json_body: Any = None
    query: Optional[dict] = None
    token: Optional[str] = None
    idempotency_key: Optional[str] = None
    request_id: Optional[str] = None

    def matches(self, method: str, path: str) -> bool:
        return self.method.upper() == method.upper() and self.path == path


_Responder = Callable[[RecordedCall], Any]


@dataclass
class _Route:
    method: str
    path: str
    responder: _Responder


class MockTransport(HTTPTransport):
    """Programmable transport that records every call."""

    def __init__(self) -> None:
        # Deliberately skip ``super().__init__`` — we never touch sockets.
        self.calls: List[RecordedCall] = []
        self._routes: List[_Route] = []
        self._queue: Deque[_Responder] = deque()
        self._default: Optional[_Responder] = None

    @property
    def base_url(self) -> str:
        return "https://mock.local"

    # ---- setup API ----

    def on(
        self,
        method: str,
        path: str,
        response: Any = None,
        *,
        responder: Optional[_Responder] = None,
    ) -> "MockTransport":
        """Register a (method, path) handler.

        Either pass a literal ``response`` (returned as-is) or a
        ``responder`` callable receiving the recorded call.
        """
        if response is not None and responder is not None:
            raise ValueError("Specify response OR responder, not both")
        if responder is None:
            fixed = response
            responder = lambda _call: fixed  # noqa: E731
        self._routes.append(
            _Route(method=method.upper(), path=path, responder=responder)
        )
        return self

    def enqueue(self, response: Any) -> "MockTransport":
        """Return ``response`` for the next unmatched call."""
        self._queue.append(lambda _call: response)
        return self

    def enqueue_error(self, exc: BaseException) -> "MockTransport":
        def _raise(_call):
            raise exc

        self._queue.append(_raise)
        return self

    def set_default(self, response: Any = None) -> "MockTransport":
        """Fall-through response when no route / queue entry matches."""
        fixed = response
        self._default = lambda _call: fixed
        return self

    # ---- introspection helpers ----

    def find(self, method: str, path: str) -> Optional[RecordedCall]:
        for call in self.calls:
            if call.matches(method, path):
                return call
        return None

    def find_all(self, method: str, path: str) -> List[RecordedCall]:
        return [c for c in self.calls if c.matches(method, path)]

    def reset(self) -> None:
        self.calls.clear()
        self._routes.clear()
        self._queue.clear()
        self._default = None

    # ---- HTTPTransport contract ----

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        query=None,
        token: Optional[str] = None,
        extra_headers=None,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> Any:
        call = RecordedCall(
            method=method.upper(),
            path=path,
            json_body=json_body,
            query=dict(query) if query else None,
            token=token,
            idempotency_key=idempotency_key,
            request_id=request_id,
        )
        self.calls.append(call)

        for route in self._routes:
            if route.method == call.method and route.path == call.path:
                return route.responder(call)

        if self._queue:
            return self._queue.popleft()(call)

        if self._default is not None:
            return self._default(call)

        return None


def make_test_client(
    transport: Optional[MockTransport] = None,
    *,
    token: Optional[str] = None,
) -> MagmaClient:
    """Return a :class:`MagmaClient` wired to a :class:`MockTransport`."""
    t = transport or MockTransport()
    return MagmaClient("https://mock.local", transport=t, token=token)
