"""SDK test fixtures — stub transport that records requests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, List, Optional

import pytest


ROOT = Path(__file__).resolve().parent.parent.parent
SDK = ROOT / "sdk"
if str(SDK) not in sys.path:
    sys.path.insert(0, str(SDK))

from magma_sdk import MagmaClient  # noqa: E402
from magma_sdk._transport import HTTPTransport  # noqa: E402


class StubTransport(HTTPTransport):
    """Replace network I/O with a programmable response queue."""

    def __init__(self):
        self.calls: List[dict] = []
        self._responder: Optional[Callable[[dict], Any]] = None

    @property
    def base_url(self) -> str:
        return "https://stub.local"

    def set_responder(self, fn: Callable[[dict], Any]) -> None:
        self._responder = fn

    def set_response(self, body: Any) -> None:
        self._responder = lambda _call: body

    def raises(self, exc: BaseException) -> None:
        def _raise(_call):
            raise exc

        self._responder = _raise

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        query=None,
        token: Optional[str] = None,
        extra_headers=None,
    ) -> Any:
        call = {
            "method": method,
            "path": path,
            "json_body": json_body,
            "query": dict(query) if query else None,
            "token": token,
        }
        self.calls.append(call)
        if self._responder is None:
            return None
        return self._responder(call)


@pytest.fixture
def transport() -> StubTransport:
    return StubTransport()


@pytest.fixture
def client(transport: StubTransport) -> MagmaClient:
    return MagmaClient("https://stub.local", transport=transport)
