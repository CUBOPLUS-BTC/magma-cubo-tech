from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import json
import base64
import time

router = APIRouter(prefix="/auth", tags=["auth"])

_challenges: dict[str, tuple[str, float]] = {}


class AuthChallenge(BaseModel):
    pubkey: str


class ChallengeResponse(BaseModel):
    challenge: str
    created_at: int


class NostrEvent(BaseModel):
    id: str
    pubkey: str
    created_at: int
    kind: int
    tags: list
    content: str
    sig: str


class VerifyRequest(BaseModel):
    signed_event: NostrEvent
    challenge: str


class VerifyResponse(BaseModel):
    pubkey: str
    success: bool


class UserResponse(BaseModel):
    pubkey: str
    created_at: int


@router.post("/challenge", response_model=ChallengeResponse)
async def get_challenge(body: AuthChallenge):
    import secrets

    challenge = secrets.token_hex(32)
    created_at = int(time.time())
    _challenges[body.pubkey] = (challenge, created_at + 120)

    return ChallengeResponse(challenge=challenge, created_at=created_at)


@router.post("/verify", response_model=VerifyResponse)
async def verify_nostr_event(body: VerifyRequest):
    from .nostr_verify import verify_nostr_event as do_verify

    event = body.signed_event

    stored = _challenges.pop(event.pubkey, None)
    if stored is None:
        raise HTTPException(status_code=401, detail="No challenge found for this pubkey")
    stored_challenge, expires_at = stored
    if stored_challenge != body.challenge:
        raise HTTPException(status_code=401, detail="Challenge mismatch")
    if time.time() > expires_at:
        raise HTTPException(status_code=401, detail="Challenge expired")

    is_valid = do_verify(event.model_dump(), body.challenge)

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid Nostr signature")

    return VerifyResponse(pubkey=event.pubkey, success=True)


@router.get("/me", response_model=UserResponse)
async def get_me(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Nostr "):
        raise HTTPException(status_code=401, detail="Missing Nostr authorization")

    try:
        event_base64 = authorization[6:]
        event_json = json.loads(base64.b64decode(event_base64).decode())
        event = event_json if isinstance(event_json, dict) else event_json

        pubkey = event.get("pubkey", "")
        if not pubkey:
            raise HTTPException(status_code=401, detail="Invalid event")

        created_at = int(time.time())
        return UserResponse(pubkey=pubkey, created_at=created_at)

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
