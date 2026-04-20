"""Tests for the MagmaClient facade: config, auth, routing."""

from __future__ import annotations

import pytest

from magma_sdk import MagmaClient, MagmaError
from magma_sdk.exceptions import AuthenticationError


class TestConstruction:
    def test_requires_http_url(self):
        with pytest.raises(MagmaError):
            MagmaClient("not-a-url")

    def test_allows_https(self):
        client = MagmaClient("https://api.test")
        assert client.token is None

    def test_allows_http(self):
        client = MagmaClient("http://localhost:8000")
        assert client.is_authenticated() is False


class TestTokenManagement:
    def test_set_token(self, client):
        client.set_token("abc")
        assert client.is_authenticated()
        assert client.token == "abc"

    def test_set_token_rejects_empty(self, client):
        with pytest.raises(MagmaError):
            client.set_token("")

    def test_set_token_rejects_non_string(self, client):
        with pytest.raises(MagmaError):
            client.set_token(123)  # type: ignore[arg-type]

    def test_clear_token(self, client):
        client.set_token("abc")
        client.clear_token()
        assert client.token is None
        assert not client.is_authenticated()


class TestAuthGating:
    def test_authed_call_without_token_raises(self, client):
        with pytest.raises(AuthenticationError):
            client.savings.progress()

    def test_authed_call_sends_token(self, transport, client):
        transport.set_response({"has_goal": False})
        client.set_token("zzz")
        client.savings.progress()
        assert transport.calls[-1]["token"] == "zzz"

    def test_public_call_sends_no_token(self, transport, client):
        transport.set_response({})
        client.remittance.fees()
        assert transport.calls[-1]["token"] is None

    def test_token_from_constructor(self, transport):
        c = MagmaClient("https://stub.local", token="init", transport=transport)
        transport.set_response({"has_goal": False})
        c.savings.progress()
        assert transport.calls[-1]["token"] == "init"
