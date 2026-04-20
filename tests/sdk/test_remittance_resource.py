"""Tests for :class:`RemittanceResource`."""

from __future__ import annotations

import pytest

from magma_sdk import MagmaError


def test_compare_parses_channels(transport, client):
    transport.set_response(
        {
            "channels": [
                {
                    "name": "Lightning Network",
                    "fee_percent": 0.3,
                    "fee_usd": 0.3,
                    "amount_received": 99.7,
                    "estimated_time": "Seconds",
                    "is_recommended": True,
                    "is_live": True,
                }
            ],
            "annual_savings": 96,
            "best_channel": "Lightning Network",
            "savings_vs_worst": 8.0,
            "worst_channel_name": "Western Union",
            "best_time": {
                "best_time": "Weekends",
                "current_fee_sat_vb": 20,
                "estimated_low_fee_sat_vb": 10,
                "savings_percent": 50,
            },
        }
    )
    result = client.remittance.compare(amount_usd=100, frequency="monthly")
    assert transport.calls[-1]["path"] == "/remittance/compare"
    assert transport.calls[-1]["json_body"] == {
        "amount_usd": 100,
        "frequency": "monthly",
    }
    assert len(result.channels) == 1
    ln = result.channels[0]
    assert ln.is_recommended is True
    assert ln.name == "Lightning Network"
    assert result.best_time is not None
    assert result.best_time.savings_percent == 50


def test_compare_missing_best_time(transport, client):
    transport.set_response(
        {
            "channels": [],
            "annual_savings": 0,
            "best_channel": "",
            "savings_vs_worst": 0,
            "worst_channel_name": "",
            "best_time": None,
        }
    )
    r = client.remittance.compare(100)
    assert r.best_time is None


def test_rejects_bad_amount(client):
    with pytest.raises(MagmaError):
        client.remittance.compare(amount_usd=0)


def test_rejects_bad_frequency(client):
    with pytest.raises(MagmaError):
        client.remittance.compare(amount_usd=100, frequency="yearly")


def test_fees_passthrough(transport, client):
    transport.set_response({"halfHourFee": 7})
    assert client.remittance.fees() == {"halfHourFee": 7}
    assert transport.calls[-1]["path"] == "/remittance/fees"
    assert transport.calls[-1]["method"] == "GET"
