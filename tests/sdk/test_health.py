"""Tests for ``MagmaClient.health`` / ``wait_until_ready`` (sync + async)."""

from __future__ import annotations

import asyncio

import pytest

from magma_sdk import MagmaError
from magma_sdk.exceptions import TransportError


class TestHealth:
    def test_returns_dict(self, transport, client):
        transport.set_response({"status": "ok", "service": "magma"})
        assert client.health() == {"status": "ok", "service": "magma"}
        assert transport.calls[-1]["path"] == "/health"

    def test_non_dict_response_normalised(self, transport, client):
        transport.set_response("not-a-dict")
        assert client.health() == {"status": "ok"}


class TestWaitUntilReady:
    def test_succeeds_immediately(self, transport, client):
        transport.set_response({"status": "ok"})
        assert client.wait_until_ready(timeout=1.0) is True

    def test_retries_until_ready(self, transport, client):
        calls = {"n": 0}

        def responder(call):
            calls["n"] += 1
            if calls["n"] < 3:
                raise TransportError("starting up")
            return {"status": "ok"}

        transport.set_responder(responder)
        sleeps = []
        now_time = {"v": 0.0}

        def now():
            return now_time["v"]

        def sleep(s):
            sleeps.append(s)
            now_time["v"] += s

        assert (
            client.wait_until_ready(
                timeout=10.0, interval=0.5, sleep=sleep, now=now
            )
            is True
        )
        assert calls["n"] == 3
        assert len(sleeps) >= 2

    def test_times_out(self, transport, client):
        transport.set_responder(lambda _c: (_ for _ in ()).throw(TransportError("down")))

        now_time = {"v": 0.0}

        def now():
            return now_time["v"]

        def sleep(s):
            now_time["v"] += s

        assert (
            client.wait_until_ready(
                timeout=1.0, interval=0.1, sleep=sleep, now=now
            )
            is False
        )

    def test_rejects_nonpositive_timeout(self, client):
        with pytest.raises(MagmaError):
            client.wait_until_ready(timeout=0)


class TestAsyncHealth:
    def test_async_health(self, transport):
        from magma_sdk import AsyncMagmaClient, MagmaClient

        sync = MagmaClient("https://stub.local", transport=transport)
        async_client = AsyncMagmaClient("https://stub.local", sync_client=sync)
        transport.set_response({"status": "ok"})

        async def go():
            return await async_client.health()

        assert asyncio.run(go()) == {"status": "ok"}

    def test_async_wait_until_ready_success(self, transport):
        from magma_sdk import AsyncMagmaClient, MagmaClient

        sync = MagmaClient("https://stub.local", transport=transport)
        async_client = AsyncMagmaClient("https://stub.local", sync_client=sync)
        transport.set_response({"status": "ok"})

        async def go():
            return await async_client.wait_until_ready(timeout=1.0)

        assert asyncio.run(go()) is True

    def test_async_wait_until_ready_timeout(self, transport):
        from magma_sdk import AsyncMagmaClient, MagmaClient

        sync = MagmaClient("https://stub.local", transport=transport)
        async_client = AsyncMagmaClient("https://stub.local", sync_client=sync)

        def boom(_c):
            raise TransportError("down")

        transport.set_responder(boom)

        async def go():
            return await async_client.wait_until_ready(
                timeout=0.1, interval=0.05
            )

        assert asyncio.run(go()) is False
