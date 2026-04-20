"""Tests for transport extensions: request-id, idempotency, on_retry."""

from __future__ import annotations

import urllib.error
from io import BytesIO
from typing import List

import pytest

from magma_sdk._transport import (
    HTTPTransport,
    IDEMPOTENCY_HEADER,
    REQUEST_ID_HEADER,
    RetryEvent,
    TransportConfig,
)


class _FakeResp:
    def __init__(self, status=200, body=b"{}", headers=None):
        self.status = status
        self._buf = BytesIO(body)
        self.headers = _FakeHeaders(headers or {})

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def getcode(self):
        return self.status

    def read(self):
        return self._buf.read()


class _FakeHeaders:
    def __init__(self, h):
        self._h = h

    def items(self):
        return self._h.items()


class TestRequestId:
    def test_generated_automatically(self):
        captured = {}

        def opener(req, timeout):
            captured["id"] = req.headers.get("X-request-id")
            return _FakeResp()

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/x")
        assert captured["id"] is not None
        assert len(captured["id"]) == 32

    def test_honours_explicit(self):
        captured = {}

        def opener(req, timeout):
            captured["id"] = req.headers.get("X-request-id")
            return _FakeResp()

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/x", request_id="abc-123")
        assert captured["id"] == "abc-123"

    def test_custom_factory(self):
        captured = {}

        def opener(req, timeout):
            captured["id"] = req.headers.get("X-request-id")
            return _FakeResp()

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(
            cfg,
            opener=opener,
            sleep=lambda _s: None,
            request_id_factory=lambda: "fixed",
        )
        t.request("GET", "/x")
        assert captured["id"] == "fixed"

    def test_constant_within_retries(self):
        ids: List[str] = []

        def opener(req, timeout):
            ids.append(req.headers.get("X-request-id"))
            if len(ids) < 2:
                return _FakeResp(status=503, body=b"{}")
            return _FakeResp()

        cfg = TransportConfig(
            base_url="https://api.test", max_retries=1, backoff=0.0
        )
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/x")
        # Same request id is reused for the retry.
        assert ids[0] == ids[1]


class TestIdempotencyKey:
    def test_header_added(self):
        captured = {}

        def opener(req, timeout):
            captured["h"] = dict(req.headers)
            return _FakeResp()

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("POST", "/x", idempotency_key="key-1")
        # urllib capitalises header names.
        assert captured["h"].get("Idempotency-key") == "key-1"

    def test_header_absent_when_none(self):
        captured = {}

        def opener(req, timeout):
            captured["h"] = dict(req.headers)
            return _FakeResp()

        cfg = TransportConfig(base_url="https://api.test", max_retries=0)
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("POST", "/x")
        assert IDEMPOTENCY_HEADER not in captured["h"]
        assert "Idempotency-key" not in captured["h"]


class TestOnRetry:
    def test_called_on_5xx_retry(self):
        events: List[RetryEvent] = []

        def opener(req, timeout):
            if len(events) == 0:
                return _FakeResp(status=503, body=b"{}")
            return _FakeResp()

        cfg = TransportConfig(
            base_url="https://api.test",
            max_retries=1,
            backoff=0.1,
            on_retry=events.append,
        )
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/x")
        assert len(events) == 1
        e = events[0]
        assert e.status == 503
        assert e.attempt == 1
        assert e.method == "GET"
        assert e.path == "/x"
        assert e.error is None
        assert e.request_id is not None

    def test_called_on_connection_error(self):
        events: List[RetryEvent] = []

        it = iter([urllib.error.URLError("net"), _FakeResp()])

        def opener(req, timeout):
            nxt = next(it)
            if isinstance(nxt, BaseException):
                raise nxt
            return nxt

        cfg = TransportConfig(
            base_url="https://api.test",
            max_retries=1,
            backoff=0.1,
            on_retry=events.append,
        )
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        t.request("GET", "/x")
        assert len(events) == 1
        assert events[0].status is None
        assert isinstance(events[0].error, urllib.error.URLError)

    def test_exception_in_hook_does_not_break(self):
        def bad_hook(_event):
            raise RuntimeError("boom")

        def opener(req, timeout):
            if not hasattr(opener, "count"):
                opener.count = 0  # type: ignore[attr-defined]
            opener.count += 1  # type: ignore[attr-defined]
            if opener.count < 2:  # type: ignore[attr-defined]
                return _FakeResp(status=503)
            return _FakeResp()

        cfg = TransportConfig(
            base_url="https://api.test",
            max_retries=1,
            backoff=0.0,
            on_retry=bad_hook,
        )
        t = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        # Should not raise despite the misbehaving hook.
        t.request("GET", "/x")


class TestClientWiresOnRetry:
    def test_client_forwards_on_retry(self):
        from magma_sdk import MagmaClient

        events: List[RetryEvent] = []

        def opener(req, timeout):
            if not hasattr(opener, "call"):
                opener.call = 0  # type: ignore[attr-defined]
            opener.call += 1  # type: ignore[attr-defined]
            if opener.call < 2:  # type: ignore[attr-defined]
                return _FakeResp(status=503)
            return _FakeResp(body=b'{"ok": true}')

        cfg = TransportConfig(
            base_url="https://api.test",
            max_retries=1,
            backoff=0.0,
            on_retry=events.append,
        )
        transport = HTTPTransport(cfg, opener=opener, sleep=lambda _s: None)
        client = MagmaClient("https://api.test", transport=transport)
        client.price.get()
        assert len(events) == 1
        assert events[0].path == "/price"
