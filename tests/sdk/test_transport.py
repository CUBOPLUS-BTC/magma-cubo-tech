"""Tests for the HTTP transport layer."""

from __future__ import annotations

import json
import urllib.error
from io import BytesIO
from typing import Any

import pytest

from magma_sdk._transport import HTTPTransport, TransportConfig
from magma_sdk.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TransportError,
    ValidationError,
)


class _FakeResp:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self._buf = BytesIO(body)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def getcode(self) -> int:
        return self.status

    def read(self) -> bytes:
        return self._buf.read()


def _transport(responses, sleeps=None, max_retries=2):
    """Build a transport whose opener yields queued responses or errors."""
    it = iter(responses)
    recorded_sleeps = sleeps if sleeps is not None else []

    def fake_opener(req, timeout):
        nxt = next(it)
        if isinstance(nxt, BaseException):
            raise nxt
        return nxt

    def fake_sleep(s):
        recorded_sleeps.append(s)

    cfg = TransportConfig(
        base_url="https://api.test",
        timeout=5.0,
        max_retries=max_retries,
        backoff=0.1,
    )
    return HTTPTransport(cfg, opener=fake_opener, sleep=fake_sleep)


class TestHappyPath:
    def test_returns_decoded_json(self):
        t = _transport([_FakeResp(200, b'{"ok": true}')])
        assert t.request("GET", "/ping") == {"ok": True}

    def test_posts_json_body(self):
        captured: dict[str, Any] = {}

        def opener(req, timeout):
            captured["url"] = req.full_url
            captured["method"] = req.get_method()
            captured["headers"] = dict(req.headers)
            captured["body"] = req.data
            return _FakeResp(200, b'{"pong": 1}')

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("POST", "/echo", json_body={"x": 1})

        assert captured["url"] == "https://api.test/echo"
        assert captured["method"] == "POST"
        assert json.loads(captured["body"].decode()) == {"x": 1}
        # urllib capitalizes header names
        assert captured["headers"].get("Content-type") == "application/json"

    def test_query_string_encoded(self):
        captured: dict[str, Any] = {}

        def opener(req, timeout):
            captured["url"] = req.full_url
            return _FakeResp(200, b"{}")

        cfg = TransportConfig(base_url="https://api.test/", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "items", query={"limit": 5, "skip": None, "q": "x y"})
        assert "limit=5" in captured["url"]
        assert "skip" not in captured["url"]
        assert "q=x+y" in captured["url"]

    def test_authorization_header(self):
        captured: dict[str, Any] = {}

        def opener(req, timeout):
            captured["auth"] = req.headers.get("Authorization")
            return _FakeResp(200, b"{}")

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/me", token="abc123")
        assert captured["auth"] == "Bearer abc123"


class TestErrors:
    def test_400_raises_validation_error(self):
        t = _transport([_FakeResp(400, b'{"detail": "bad"}')], max_retries=0)
        with pytest.raises(ValidationError) as exc:
            t.request("GET", "/x")
        assert exc.value.status == 400
        assert exc.value.detail == "bad"

    def test_401_raises_auth_error(self):
        t = _transport([_FakeResp(401, b'{"detail": "nope"}')], max_retries=0)
        with pytest.raises(AuthenticationError):
            t.request("GET", "/x")

    def test_404_raises_not_found(self):
        t = _transport([_FakeResp(404, b'{"detail": "missing"}')], max_retries=0)
        with pytest.raises(NotFoundError):
            t.request("GET", "/x")

    def test_429_retried_then_succeeds(self):
        sleeps: list[float] = []
        t = _transport(
            [
                _FakeResp(429, b'{"detail": "slow down"}'),
                _FakeResp(200, b'{"ok": true}'),
            ],
            sleeps=sleeps,
            max_retries=2,
        )
        assert t.request("GET", "/x") == {"ok": True}
        assert len(sleeps) == 1

    def test_429_retries_exhausted(self):
        sleeps: list[float] = []
        t = _transport(
            [
                _FakeResp(429, b"{}"),
                _FakeResp(429, b"{}"),
                _FakeResp(429, b"{}"),
            ],
            sleeps=sleeps,
            max_retries=2,
        )
        with pytest.raises(RateLimitError):
            t.request("GET", "/x")

    def test_500_retries_then_fails(self):
        t = _transport(
            [_FakeResp(500, b"{}"), _FakeResp(500, b"{}"), _FakeResp(500, b"{}")],
            max_retries=2,
        )
        with pytest.raises(ServerError) as exc:
            t.request("GET", "/x")
        assert exc.value.status == 500

    def test_http_error_decoded(self):
        err = urllib.error.HTTPError(
            "https://api.test/x", 404, "Not Found", {}, BytesIO(b'{"detail": "gone"}')
        )
        t = _transport([err], max_retries=0)
        with pytest.raises(NotFoundError) as exc:
            t.request("GET", "/x")
        assert exc.value.detail == "gone"

    def test_connection_error_raises_transport(self):
        t = _transport(
            [urllib.error.URLError("net"), urllib.error.URLError("net")],
            max_retries=1,
        )
        with pytest.raises(TransportError):
            t.request("GET", "/x")

    def test_connection_error_retried_then_succeeds(self):
        t = _transport(
            [urllib.error.URLError("net"), _FakeResp(200, b'{"v": 1}')],
            max_retries=1,
        )
        assert t.request("GET", "/x") == {"v": 1}

    def test_non_json_response(self):
        t = _transport([_FakeResp(200, b"<html></html>")], max_retries=0)
        with pytest.raises(TransportError):
            t.request("GET", "/x")

    def test_timeout_raises_transport(self):
        t = _transport(
            [TimeoutError("slow"), TimeoutError("slow")], max_retries=1
        )
        with pytest.raises(TransportError):
            t.request("GET", "/x")

    def test_generic_api_error_for_418(self):
        t = _transport([_FakeResp(418, b'{"detail": "teapot"}')], max_retries=0)
        with pytest.raises(APIError) as exc:
            t.request("GET", "/x")
        assert exc.value.status == 418
