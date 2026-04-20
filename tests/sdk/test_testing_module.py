"""Tests for :mod:`magma_sdk.testing` — consumer-facing helpers."""

from __future__ import annotations

import pytest

from magma_sdk.testing import MockTransport, make_test_client


class TestMockTransport:
    def test_on_route_returns_response(self):
        mock = MockTransport()
        mock.on("GET", "/price", {"price_usd": 70000})
        client = make_test_client(transport=mock)
        assert client.price.get().price_usd == 70000

    def test_records_calls(self):
        mock = MockTransport()
        mock.on("GET", "/price", {"price_usd": 1, "sources_count": 1, "deviation": 0, "has_warning": False})
        client = make_test_client(transport=mock)
        client.price.get()
        assert len(mock.calls) == 1
        assert mock.calls[0].method == "GET"
        assert mock.calls[0].path == "/price"
        assert mock.find("GET", "/price") is not None

    def test_enqueue_fallback(self):
        mock = MockTransport()
        mock.enqueue({"status": "ok"})
        client = make_test_client(transport=mock)
        assert client.health() == {"status": "ok"}

    def test_default_response(self):
        mock = MockTransport()
        mock.set_default({})
        client = make_test_client(transport=mock)
        # No route, no queue — fall back to default.
        assert client.remittance.fees() == {}

    def test_enqueue_error(self):
        from magma_sdk.exceptions import TransportError

        mock = MockTransport()
        mock.enqueue_error(TransportError("boom"))
        client = make_test_client(transport=mock)
        with pytest.raises(TransportError):
            client.price.get()

    def test_responder_sees_recorded_call(self):
        mock = MockTransport()

        def responder(call):
            assert call.method == "POST"
            assert call.path == "/savings/deposit"
            assert call.json_body == {"amount_usd": 50}
            return {"ok": True}

        mock.on("POST", "/savings/deposit", responder=responder)
        client = make_test_client(transport=mock, token="t")
        assert client.savings.record_deposit(50) == {"ok": True}

    def test_reject_both_response_and_responder(self):
        mock = MockTransport()
        with pytest.raises(ValueError):
            mock.on("GET", "/x", {}, responder=lambda _c: {})

    def test_find_all(self):
        mock = MockTransport()
        mock.set_default({})
        client = make_test_client(transport=mock)
        client.remittance.fees()
        client.remittance.fees()
        assert len(mock.find_all("GET", "/remittance/fees")) == 2

    def test_reset(self):
        mock = MockTransport()
        mock.on("GET", "/x", {})
        mock.enqueue({})
        mock.set_default({})
        client = make_test_client(transport=mock)
        client.health()
        mock.reset()
        assert mock.calls == []
        assert mock.find("GET", "/x") is None

    def test_base_url_property(self):
        mock = MockTransport()
        assert mock.base_url.startswith("https://mock.local")

    def test_idempotency_key_recorded(self):
        mock = MockTransport()
        mock.set_default({"ok": True})
        client = make_test_client(transport=mock, token="t")
        client.savings.record_deposit(10, idempotency_key="abc-1")
        assert mock.calls[0].idempotency_key == "abc-1"

    def test_request_id_recorded(self):
        mock = MockTransport()
        mock.set_default({"ok": True})
        client = make_test_client(transport=mock)
        client._request("GET", "/health", request_id="rid-99")
        assert mock.calls[0].request_id == "rid-99"

    def test_make_test_client_stores_token(self):
        client = make_test_client(token="hello")
        assert client.token == "hello"
