"""Tests for :class:`PensionResource`."""

from __future__ import annotations

import pytest

from magma_sdk import MagmaError


def test_project_sends_and_parses(transport, client):
    transport.set_response(
        {
            "total_invested_usd": 24000,
            "total_btc_accumulated": 0.4,
            "current_value_usd": 36000,
            "avg_buy_price": 60000,
            "current_btc_price": 70000,
            "monthly_breakdown": [{"month": 1}],
            "monthly_data": [{"month": 1}],
        }
    )
    result = client.pension.project(monthly_saving_usd=100, years=20)
    call = transport.calls[-1]
    assert call["method"] == "POST"
    assert call["path"] == "/pension/projection"
    assert call["json_body"] == {"monthly_saving_usd": 100, "years": 20}
    assert result.total_invested_usd == 24000
    assert result.total_btc_accumulated == 0.4


@pytest.mark.parametrize("value", [0, -10, float("inf"), True])
def test_rejects_bad_monthly(client, value):
    with pytest.raises(MagmaError):
        client.pension.project(monthly_saving_usd=value, years=10)


@pytest.mark.parametrize("years", [0, -1, True, 1.5])
def test_rejects_bad_years(client, years):
    with pytest.raises(MagmaError):
        client.pension.project(monthly_saving_usd=100, years=years)
