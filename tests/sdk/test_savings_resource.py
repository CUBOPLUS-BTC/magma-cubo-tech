"""Tests for :class:`SavingsResource`."""

from __future__ import annotations

import pytest

from magma_sdk import MagmaError


class TestProject:
    def test_sends_correct_request(self, transport, client):
        transport.set_response(
            {
                "monthly_usd": 100,
                "years": 10,
                "total_invested": 12000,
                "current_btc_price": 50000,
                "scenarios": [],
                "traditional_value": 15000,
                "monthly_data": [],
            }
        )
        result = client.savings.project(monthly_usd=100, years=10)
        assert transport.calls[-1]["method"] == "POST"
        assert transport.calls[-1]["path"] == "/savings/project"
        assert transport.calls[-1]["json_body"] == {
            "monthly_usd": 100,
            "years": 10,
        }
        assert result.monthly_usd == 100
        assert result.years == 10
        assert result.total_invested == 12000
        assert result.traditional_value == 15000

    def test_parses_scenarios(self, transport, client):
        transport.set_response(
            {
                "scenarios": [
                    {
                        "name": "conservative",
                        "annual_return_pct": 5,
                        "total_invested": 1200,
                        "projected_value": 1500,
                        "total_btc": 0.02,
                        "multiplier": 1.25,
                    }
                ]
            }
        )
        result = client.savings.project(monthly_usd=10, years=1)
        assert len(result.scenarios) == 1
        s = result.scenarios[0]
        assert s.name == "conservative"
        assert s.annual_return_pct == 5
        assert s.multiplier == 1.25

    @pytest.mark.parametrize("value", [0, -1, float("nan"), True])
    def test_rejects_bad_monthly(self, client, value):
        with pytest.raises(MagmaError):
            client.savings.project(monthly_usd=value, years=5)

    @pytest.mark.parametrize("years", [0, 51, -1, True, 1.5])
    def test_rejects_bad_years(self, client, years):
        with pytest.raises(MagmaError):
            client.savings.project(monthly_usd=100, years=years)


class TestCreateGoal:
    def test_sends_auth_request(self, transport, client):
        client.set_token("t")
        transport.set_response({"ok": True})
        client.savings.create_goal(monthly_target_usd=50, target_years=10)
        call = transport.calls[-1]
        assert call["path"] == "/savings/goal"
        assert call["method"] == "POST"
        assert call["token"] == "t"
        assert call["json_body"] == {
            "monthly_target_usd": 50,
            "target_years": 10,
        }

    def test_requires_token(self, client):
        from magma_sdk.exceptions import AuthenticationError

        with pytest.raises(AuthenticationError):
            client.savings.create_goal(monthly_target_usd=50)


class TestRecordDeposit:
    def test_happy_path(self, transport, client):
        client.set_token("t")
        transport.set_response({"amount_usd": 25, "btc_price": 50000})
        result = client.savings.record_deposit(amount_usd=25)
        assert result["amount_usd"] == 25
        assert transport.calls[-1]["json_body"] == {"amount_usd": 25}

    def test_rejects_zero(self, client):
        client.set_token("t")
        with pytest.raises(MagmaError):
            client.savings.record_deposit(amount_usd=0)


class TestProgress:
    def test_parses_progress(self, transport, client):
        client.set_token("t")
        transport.set_response(
            {
                "has_goal": True,
                "total_invested_usd": 1200,
                "total_btc": 0.05,
                "current_value_usd": 1300,
                "roi_percent": 8.3,
                "streak_months": 4,
                "deposit_count": 12,
                "recent_deposits": [{"amount_usd": 100}],
                "milestones": [],
            }
        )
        p = client.savings.progress()
        assert p.has_goal is True
        assert p.streak_months == 4
        assert p.total_invested_usd == 1200
        assert p.recent_deposits == [{"amount_usd": 100}]
