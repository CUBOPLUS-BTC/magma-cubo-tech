import json
import base64
import time
import secrets

_challenges: dict[str, tuple[str, float]] = {}


def handle_challenge(body: dict) -> tuple[dict, int]:
    """POST /auth/challenge"""
    pubkey = body.get("pubkey", "")
    if not pubkey:
        return {"detail": "pubkey is required"}, 400

    challenge = secrets.token_hex(32)
    created_at = int(time.time())
    _challenges[pubkey] = (challenge, created_at + 120)

    return {"challenge": challenge, "created_at": created_at}, 200


def handle_verify(body: dict) -> tuple[dict, int]:
    """POST /auth/verify"""
    from .nostr_verify import verify_nostr_event as do_verify

    event_data = body.get("signed_event", {})
    challenge = body.get("challenge", "")

    pubkey = event_data.get("pubkey", "")
    if not pubkey:
        return {"detail": "Missing pubkey in signed_event"}, 401

    stored = _challenges.pop(pubkey, None)
    if stored is None:
        return {"detail": "No challenge found for this pubkey"}, 401

    stored_challenge, expires_at = stored
    if stored_challenge != challenge:
        return {"detail": "Challenge mismatch"}, 401
    if time.time() > expires_at:
        return {"detail": "Challenge expired"}, 401

    is_valid = do_verify(event_data, challenge)
    if not is_valid:
        return {"detail": "Invalid Nostr signature"}, 401

    return {"pubkey": pubkey, "success": True}, 200


def handle_me(authorization: str) -> tuple[dict, int]:
    """GET /auth/me"""
    if not authorization or not authorization.startswith("Nostr "):
        return {"detail": "Missing Nostr authorization"}, 401

    try:
        event_base64 = authorization[6:]
        event_json = json.loads(base64.b64decode(event_base64).decode())
        event = event_json if isinstance(event_json, dict) else {}

        pubkey = event.get("pubkey", "")
        if not pubkey:
            return {"detail": "Invalid event"}, 401

        return {"pubkey": pubkey, "created_at": int(time.time())}, 200

    except Exception:
        return {"detail": "Invalid authorization header"}, 401
