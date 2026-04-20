"""Tests for :class:`AlertsResource`, :class:`PriceResource`,
:class:`NetworkResource`, and :class:`GamificationResource`."""

from __future__ import annotations

import pytest

from magma_sdk.exceptions import AuthenticationError


class TestAlerts:
    def test_list_parses_alerts(self, transport, client):
        transport.set_response(
            {
                "alerts": [
                    {
                        "type": "fee_low",
                        "message": "Low fees",
                        "created_at": 1700000000,
                    },
                    "ignored",
                ]
            }
        )
        alerts = client.alerts.list(limit=5)
        assert transport.calls[-1]["query"] == {"limit": 5}
        assert len(alerts) == 1
        assert alerts[0].type == "fee_low"
        assert alerts[0].created_at == 1700000000

    def test_list_normalizes_bad_limit(self, transport, client):
        transport.set_response({"alerts": []})
        client.alerts.list(limit=-1)
        assert transport.calls[-1]["query"] == {"limit": 20}

    def test_status_passthrough(self, transport, client):
        transport.set_response({"running": True})
        assert client.alerts.status() == {"running": True}


class TestPrice:
    def test_get_parses(self, transport, client):
        transport.set_response(
            {
                "price_usd": 70000.5,
                "sources_count": 2,
                "deviation": 0.1,
                "has_warning": False,
            }
        )
        p = client.price.get()
        assert p.price_usd == 70000.5
        assert p.sources_count == 2
        assert p.has_warning is False

    def test_get_handles_non_dict(self, transport, client):
        transport.set_response(None)
        p = client.price.get()
        assert p.price_usd == 0.0


class TestNetwork:
    def test_status_passthrough(self, transport, client):
        transport.set_response({"height": 800000})
        assert client.network.status() == {"height": 800000}
        assert transport.calls[-1]["path"] == "/network/status"


class TestGamification:
    def test_requires_token(self, client):
        with pytest.raises(AuthenticationError):
            client.gamification.achievements()

    def test_sends_token(self, transport, client):
        client.set_token("abc")
        transport.set_response({"achievements": [], "level": 1})
        result = client.gamification.achievements()
        assert result["level"] == 1
        assert transport.calls[-1]["token"] == "abc"
