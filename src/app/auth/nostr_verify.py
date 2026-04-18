import json
import hashlib
import logging
import time

logger = logging.getLogger(__name__)


def verify_nostr_event(event: dict, expected_challenge: str) -> bool:
    try:
        pubkey = event.get("pubkey", "")
        created_at = event.get("created_at", 0)
        kind = event.get("kind", 0)
        tags = event.get("tags", [])
        content = event.get("content", "")
        sig = event.get("sig", "")
        event_id = event.get("id", "")

        if kind != 27235:
            return False

        if abs(int(time.time()) - created_at) > 120:
            return False

        if content != expected_challenge:
            return False

        tag_dict = {t[0]: t[1:] for t in tags if len(t) >= 2}
        if "u" not in tag_dict or "method" not in tag_dict:
            return False

        serialized = json.dumps(
            [0, pubkey, created_at, kind, tags, content], separators=(",", ":")
        )
        computed_id = hashlib.sha256(serialized.encode()).hexdigest()

        if computed_id != event_id:
            return False

        if not _verify_schnorr_signature(pubkey, computed_id, sig):
            return False

        return True

    except Exception as e:
        logger.exception("Verification error: %s", e)
        return False


def verify_nip98_event(event: dict, expected_url: str, expected_method: str) -> bool:
    """Verify NIP-98 HTTP Auth event. Unlike verify_nostr_event, does NOT check content."""
    try:
        pubkey = event.get("pubkey", "")
        created_at = event.get("created_at", 0)
        kind = event.get("kind", 0)
        tags = event.get("tags", [])
        content = event.get("content", "")
        sig = event.get("sig", "")
        event_id = event.get("id", "")

        if kind != 27235:
            return False

        if abs(int(time.time()) - created_at) > 120:
            return False

        tag_dict = {t[0]: t[1] for t in tags if len(t) >= 2}
        if "u" not in tag_dict or "method" not in tag_dict:
            return False

        if not tag_dict["u"].startswith(expected_url):
            return False
        if tag_dict["method"].upper() != expected_method.upper():
            return False

        serialized = json.dumps(
            [0, pubkey, created_at, kind, tags, content], separators=(",", ":")
        )
        computed_id = hashlib.sha256(serialized.encode()).hexdigest()

        if computed_id != event_id:
            return False

        return _verify_schnorr_signature(pubkey, computed_id, sig)

    except Exception as e:
        logger.exception("NIP-98 verification error: %s", e)
        return False


def _verify_schnorr_signature(pubkey_hex: str, msg_hash: str, sig_hex: str) -> bool:
    try:
        from coincurve import PublicKeyXOnly

        pubkey = PublicKeyXOnly(bytes.fromhex(pubkey_hex))
        return pubkey.verify(bytes.fromhex(sig_hex), bytes.fromhex(msg_hash))

    except Exception as e:
        logger.exception("Schnorr verification error: %s", e)
        return False
