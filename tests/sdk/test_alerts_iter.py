"""Tests for ``AlertsResource.iter_new`` and the async ``stream``."""

from __future__ import annotations

import asyncio
from typing import List

import pytest


def _alert(ts, msg="m", typ="t"):
    return {"type": typ, "message": msg, "created_at": ts}


class TestIterNew:
    def test_emits_oldest_first(self, transport, client):
        # /alerts returns "most recent first", we normalise back to chronological.
        transport.set_response(
            {"alerts": [_alert(3, "c"), _alert(2, "b"), _alert(1, "a")]}
        )
        sleeps: List[float] = []
        it = client.alerts.iter_new(
            poll_interval=0.0,
            max_iterations=1,
            sleep=sleeps.append,
        )
        msgs = [a.message for a in it]
        assert msgs == ["a", "b", "c"]

    def test_respects_since_cursor(self, transport, client):
        transport.set_response(
            {"alerts": [_alert(3, "c"), _alert(2, "b"), _alert(1, "a")]}
        )
        it = client.alerts.iter_new(
            since=2, poll_interval=0.0, max_iterations=1, sleep=lambda _s: None
        )
        msgs = [a.message for a in it]
        assert msgs == ["c"]

    def test_deduplicates_across_polls(self, transport, client):
        responses = iter(
            [
                {"alerts": [_alert(1, "a"), _alert(2, "b")]},
                {"alerts": [_alert(2, "b"), _alert(3, "c")]},
            ]
        )

        def responder(call):
            return next(responses)

        transport.set_responder(responder)
        it = client.alerts.iter_new(
            poll_interval=0.0, max_iterations=2, sleep=lambda _s: None
        )
        msgs = [a.message for a in it]
        assert msgs == ["a", "b", "c"]

    def test_stop_predicate(self, transport, client):
        transport.set_response({"alerts": [_alert(1, "a")]})
        stop_flag = {"v": False}

        def stop():
            if not stop_flag["v"]:
                stop_flag["v"] = True
                return False
            return True

        it = client.alerts.iter_new(
            poll_interval=0.0, sleep=lambda _s: None, stop=stop
        )
        msgs = [a.message for a in it]
        # First iteration emits 'a'; second iteration re-fetches the same
        # alert (deduped) and then stop() returns True.
        assert msgs == ["a"]

    def test_negative_poll_interval(self, client):
        with pytest.raises(ValueError):
            list(client.alerts.iter_new(poll_interval=-1, max_iterations=1))


def _run(coro):
    return asyncio.run(coro)


class TestAsyncStream:
    def test_stream_uses_async_sleep(self):
        from magma_sdk import AsyncMagmaClient, MagmaClient
        from tests.sdk.conftest import StubTransport

        transport = StubTransport()
        sync = MagmaClient("https://stub.local", transport=transport)
        async_client = AsyncMagmaClient("https://stub.local", sync_client=sync)

        responses = iter(
            [
                {"alerts": [_alert(1, "a")]},
                {"alerts": [_alert(2, "b")]},
            ]
        )
        transport.set_responder(lambda _c: next(responses))

        async def collect():
            out = []
            async for alert in async_client.alerts.stream(
                poll_interval=0.0, max_iterations=2
            ):
                out.append(alert.message)
            return out

        assert _run(collect()) == ["a", "b"]

    def test_stream_respects_since(self):
        from magma_sdk import AsyncMagmaClient, MagmaClient
        from tests.sdk.conftest import StubTransport

        transport = StubTransport()
        sync = MagmaClient("https://stub.local", transport=transport)
        async_client = AsyncMagmaClient("https://stub.local", sync_client=sync)
        transport.set_response(
            {"alerts": [_alert(1, "a"), _alert(2, "b")]}
        )

        async def collect():
            out = []
            async for alert in async_client.alerts.stream(
                since=1, poll_interval=0.0, max_iterations=1
            ):
                out.append(alert.message)
            return out

        assert _run(collect()) == ["b"]

    def test_negative_interval_rejected(self):
        from magma_sdk import AsyncMagmaClient, MagmaClient
        from tests.sdk.conftest import StubTransport

        transport = StubTransport()
        sync = MagmaClient("https://stub.local", transport=transport)
        client = AsyncMagmaClient("https://stub.local", sync_client=sync)

        async def run():
            async for _ in client.alerts.stream(poll_interval=-1):
                pass

        with pytest.raises(ValueError):
            _run(run())
