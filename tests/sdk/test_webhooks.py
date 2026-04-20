"""Tests for :mod:`magma_sdk.webhooks`."""

from __future__ import annotations

import json

import pytest

from magma_sdk.webhooks import (
    InvalidSignatureError,
    MalformedWebhookError,
    ReplayError,
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    WebhookEvent,
    WebhookVerifier,
    sign,
)


SECRET = "top-secret"
BODY = json.dumps({"type": "alert.fee_low", "data": {"sat_vb": 3}}).encode()


class TestSign:
    def test_sign_returns_both_headers(self):
        headers = sign(BODY, SECRET, timestamp=1700000000)
        assert SIGNATURE_HEADER in headers
        assert headers[TIMESTAMP_HEADER] == "1700000000"

    def test_deterministic(self):
        a = sign(BODY, SECRET, timestamp=1700000000)
        b = sign(BODY, SECRET, timestamp=1700000000)
        assert a == b

    def test_different_body_changes_signature(self):
        a = sign(b"one", SECRET, timestamp=1700000000)
        b = sign(b"two", SECRET, timestamp=1700000000)
        assert a[SIGNATURE_HEADER] != b[SIGNATURE_HEADER]

    def test_accepts_str_body_and_secret(self):
        sign("hello", "key", timestamp=1)

    def test_missing_secret(self):
        with pytest.raises(MalformedWebhookError):
            sign(BODY, "", timestamp=1700000000)


class TestVerifier:
    def test_round_trip(self):
        verifier = WebhookVerifier(SECRET)
        headers = sign(BODY, SECRET, timestamp=1700000000)
        event = verifier.verify(
            body=BODY,
            signature=headers[SIGNATURE_HEADER],
            timestamp=headers[TIMESTAMP_HEADER],
            now=1700000000,
        )
        assert isinstance(event, WebhookEvent)
        assert event.type == "alert.fee_low"
        assert event.data == {"sat_vb": 3}
        assert event.timestamp == 1700000000

    def test_rejects_tampered_body(self):
        verifier = WebhookVerifier(SECRET)
        headers = sign(BODY, SECRET, timestamp=1700000000)
        with pytest.raises(InvalidSignatureError):
            verifier.verify(
                body=b"tampered",
                signature=headers[SIGNATURE_HEADER],
                timestamp=headers[TIMESTAMP_HEADER],
                now=1700000000,
            )

    def test_rejects_wrong_secret(self):
        v1 = WebhookVerifier("key-a")
        headers = sign(BODY, "key-b", timestamp=1700000000)
        with pytest.raises(InvalidSignatureError):
            v1.verify(
                body=BODY,
                signature=headers[SIGNATURE_HEADER],
                timestamp=headers[TIMESTAMP_HEADER],
                now=1700000000,
            )

    def test_replay_beyond_tolerance(self):
        verifier = WebhookVerifier(SECRET, tolerance_seconds=300)
        headers = sign(BODY, SECRET, timestamp=1700000000)
        with pytest.raises(ReplayError):
            verifier.verify(
                body=BODY,
                signature=headers[SIGNATURE_HEADER],
                timestamp=headers[TIMESTAMP_HEADER],
                now=1700000000 + 301,
            )

    def test_replay_inside_tolerance_ok(self):
        verifier = WebhookVerifier(SECRET, tolerance_seconds=300)
        headers = sign(BODY, SECRET, timestamp=1700000000)
        event = verifier.verify(
            body=BODY,
            signature=headers[SIGNATURE_HEADER],
            timestamp=headers[TIMESTAMP_HEADER],
            now=1700000000 + 299,
        )
        assert event.type == "alert.fee_low"

    def test_verify_request_case_insensitive_headers(self):
        verifier = WebhookVerifier(SECRET)
        headers = sign(BODY, SECRET, timestamp=1700000000)
        mixed = {
            "x-magma-signature": headers[SIGNATURE_HEADER],
            "X-MAGMA-TIMESTAMP": headers[TIMESTAMP_HEADER],
            "other": "ignored",
        }
        event = verifier.verify_request(BODY, mixed, now=1700000000)
        assert event.timestamp == 1700000000

    def test_verify_request_missing_headers(self):
        verifier = WebhookVerifier(SECRET)
        with pytest.raises(MalformedWebhookError):
            verifier.verify_request(BODY, {}, now=1700000000)

    def test_invalid_json_body(self):
        verifier = WebhookVerifier(SECRET)
        headers = sign(b"not json", SECRET, timestamp=1700000000)
        with pytest.raises(MalformedWebhookError):
            verifier.verify(
                body=b"not json",
                signature=headers[SIGNATURE_HEADER],
                timestamp=headers[TIMESTAMP_HEADER],
                now=1700000000,
            )

    def test_non_object_json_body(self):
        verifier = WebhookVerifier(SECRET)
        body = b"[1, 2, 3]"
        headers = sign(body, SECRET, timestamp=1700000000)
        with pytest.raises(MalformedWebhookError):
            verifier.verify(
                body=body,
                signature=headers[SIGNATURE_HEADER],
                timestamp=headers[TIMESTAMP_HEADER],
                now=1700000000,
            )

    def test_non_integer_timestamp(self):
        verifier = WebhookVerifier(SECRET)
        with pytest.raises(ReplayError):
            verifier.verify(
                body=BODY,
                signature="deadbeef",
                timestamp="not-a-number",
                now=1700000000,
            )

    def test_parse_false_skips_payload(self):
        verifier = WebhookVerifier(SECRET)
        body = b"abc"
        headers = sign(body, SECRET, timestamp=1700000000)
        event = verifier.verify(
            body=body,
            signature=headers[SIGNATURE_HEADER],
            timestamp=headers[TIMESTAMP_HEADER],
            now=1700000000,
            parse=False,
        )
        assert event.type == ""
        assert event.raw == {}

    def test_rejects_empty_signature(self):
        verifier = WebhookVerifier(SECRET)
        with pytest.raises(InvalidSignatureError):
            verifier.verify(body=BODY, signature="", timestamp="1700000000")

    def test_invalid_secret_construction(self):
        with pytest.raises(MalformedWebhookError):
            WebhookVerifier("")

    def test_invalid_tolerance(self):
        with pytest.raises(MalformedWebhookError):
            WebhookVerifier(SECRET, tolerance_seconds=-1)
