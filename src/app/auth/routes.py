import json
import base64
import time
import secrets

from .lnurl import create_lnurl_challenge, verify_lnurl_callback, get_lnurl_status
from .sessions import create_session, validate_session
from ..validation import validate_pubkey

_challenges: dict[str, tuple[str, float]] = {}
_rate_limits: dict[str, list[float]] = {}


def handle_challenge(body: dict) -> tuple[dict, int]:
    """POST /auth/challenge"""
    pubkey = body.get("pubkey", "")
    if not pubkey:
        return {"detail": "pubkey is required"}, 400

    if not validate_pubkey(pubkey):
        return {"detail": "Invalid pubkey format"}, 400

    now = time.time()
    if pubkey in _rate_limits:
        _rate_limits[pubkey] = [t for t in _rate_limits[pubkey] if now - t < 60]
        if len(_rate_limits[pubkey]) >= 5:
            return {"detail": "Too many requests"}, 429
    else:
        _rate_limits[pubkey] = []

    _rate_limits[pubkey].append(now)

    challenge = secrets.token_hex(32)
    created_at = int(time.time())
    _challenges[pubkey] = (challenge, created_at + 120)

    return {"challenge": challenge, "created_at": created_at}, 200


def handle_verify(body: dict) -> tuple[dict, int]:
    """POST /auth/verify — Verify NIP-07 signed event and create session."""
    from .nostr_verify import verify_nostr_event as do_verify

    event_data = body.get("signed_event", {})
    challenge = body.get("challenge", "")

    pubkey = event_data.get("pubkey", "")
    if not pubkey:
        return {"detail": "Missing pubkey in signed_event"}, 401

    if not validate_pubkey(pubkey):
        return {"detail": "Invalid pubkey format"}, 401

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

    token = create_session(pubkey)

    # Upsert user in database
    try:
        from ..database import get_conn, _is_postgres

        conn = get_conn()
        now = int(time.time())
        if _is_postgres():
            conn.execute(
                "INSERT INTO users (pubkey, auth_method, created_at) VALUES (%s, 'nostr', %s) ON CONFLICT (pubkey) DO NOTHING",
                (pubkey, now),
            )
        else:
            conn.execute(
                "INSERT OR IGNORE INTO users (pubkey, auth_method, created_at) VALUES (?, 'nostr', ?)",
                (pubkey, now),
            )
        conn.commit()
    except Exception:
        pass

    return {"status": "ok", "token": token, "pubkey": pubkey}, 200


def handle_me(
    authorization: str, url: str = "", method: str = "GET"
) -> tuple[dict, int]:
    """GET /auth/me — supports both Nostr and Bearer token auth"""
    if not authorization:
        return {"detail": "Missing authorization"}, 401

    # Bearer token (LNURL-auth sessions)
    if authorization.startswith("Bearer "):
        token = authorization[7:]
        pubkey = validate_session(token)
        if pubkey is None:
            return {"detail": "Invalid or expired token"}, 401
        return {"pubkey": pubkey, "created_at": int(time.time())}, 200

    # Nostr auth (NIP-98)
    if authorization.startswith("Nostr "):
        try:
            event_base64 = authorization[6:]
            event_json = json.loads(base64.b64decode(event_base64).decode())
            event = event_json if isinstance(event_json, dict) else {}
            pubkey = event.get("pubkey", "")
            if not pubkey:
                return {"detail": "Invalid event"}, 401
            from .nostr_verify import verify_nip98_event

            if not verify_nip98_event(event, url, method):
                return {"detail": "Invalid Nostr signature"}, 401
            return {"pubkey": pubkey, "created_at": int(time.time())}, 200
        except Exception:
            return {"detail": "Invalid authorization header"}, 401

    return {"detail": "Unsupported authorization method"}, 401


def handle_lnurl_create(body: dict) -> tuple[dict, int]:
    """POST /auth/lnurl — Generate LNURL-auth QR challenge."""
    result = create_lnurl_challenge()
    return result, 200


def handle_lnurl_callback(query: dict) -> tuple[dict, int]:
    """GET /auth/lnurl-callback?tag=login&k1=...&sig=...&key=... — Called by wallet."""
    tag = query.get("tag", "")
    k1 = query.get("k1", "")
    sig = query.get("sig", "")
    key = query.get("key", "")

    if tag != "login":
        return {"status": "ERROR", "reason": "Invalid tag"}, 200

    if not all([k1, sig, key]):
        return {"status": "ERROR", "reason": "Missing parameters"}, 200

    success = verify_lnurl_callback(k1, sig, key)
    if success:
        return {"status": "OK"}, 200
    else:
        return {"status": "ERROR", "reason": "Signature verification failed"}, 200


def handle_lnurl_status(query: dict) -> tuple[dict, int]:
    """GET /auth/lnurl-status?k1=... — Frontend polls this."""
    k1 = query.get("k1", "")
    if not k1:
        return {"detail": "k1 is required"}, 400

    result = get_lnurl_status(k1)
    return result, 200
