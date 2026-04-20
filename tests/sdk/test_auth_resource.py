"""Tests for :class:`AuthResource`."""

from __future__ import annotations

import pytest

from magma_sdk import MagmaError


VALID_PUBKEY = "a" * 64


class TestChallenge:
    def test_create_challenge(self, transport, client):
        transport.set_response({"challenge": "deadbeef", "created_at": 1700000000})
        c = client.auth.create_challenge(VALID_PUBKEY)
        call = transport.calls[-1]
        assert call["path"] == "/auth/challenge"
        assert call["json_body"] == {"pubkey": VALID_PUBKEY}
        assert c.challenge == "deadbeef"
        assert c.created_at == 1700000000

    def test_rejects_short_pubkey(self, client):
        with pytest.raises(MagmaError):
            client.auth.create_challenge("short")


class TestVerify:
    def test_stores_token_on_success(self, transport, client):
        transport.set_response({"token": "tok", "pubkey": VALID_PUBKEY})
        session = client.auth.verify(
            signed_event={"pubkey": VALID_PUBKEY, "sig": "x"},
            challenge="c1",
        )
        assert session.token == "tok"
        assert client.token == "tok"
        assert client.is_authenticated()

    def test_raises_when_no_token_returned(self, transport, client):
        transport.set_response({"token": "", "pubkey": VALID_PUBKEY})
        with pytest.raises(MagmaError):
            client.auth.verify({"pubkey": VALID_PUBKEY}, challenge="c1")

    def test_rejects_missing_pubkey(self, client):
        with pytest.raises(MagmaError):
            client.auth.verify(signed_event={}, challenge="c1")

    def test_rejects_empty_challenge(self, client):
        with pytest.raises(MagmaError):
            client.auth.verify({"pubkey": VALID_PUBKEY}, challenge="")


class TestLnurl:
    def test_create_lnurl(self, transport, client):
        transport.set_response({"k1": "beef", "lnurl": "LNURL1..."})
        lc = client.auth.create_lnurl()
        assert lc.k1 == "beef"
        assert lc.lnurl == "LNURL1..."
        assert transport.calls[-1]["path"] == "/auth/lnurl"

    def test_lnurl_status_stores_token_when_authenticated(self, transport, client):
        transport.set_response(
            {"token": "t", "pubkey": VALID_PUBKEY}
        )
        status = client.auth.lnurl_status("beef")
        assert status.authenticated is True
        assert status.token == "t"
        assert client.token == "t"

    def test_lnurl_status_pending(self, transport, client):
        transport.set_response({"status": "PENDING"})
        status = client.auth.lnurl_status("beef")
        assert status.authenticated is False
        assert status.token is None
        assert client.token is None

    def test_lnurl_status_requires_k1(self, client):
        with pytest.raises(MagmaError):
            client.auth.lnurl_status("")
