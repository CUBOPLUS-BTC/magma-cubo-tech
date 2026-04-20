"""Authentication endpoints: Nostr (NIP-07) and LNURL-auth."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..exceptions import MagmaError
from ._base import Resource


@dataclass(frozen=True)
class Challenge:
    challenge: str
    created_at: int


@dataclass(frozen=True)
class AuthSession:
    token: str
    pubkey: str


@dataclass(frozen=True)
class LnurlChallenge:
    k1: str
    lnurl: str
    raw: dict


@dataclass(frozen=True)
class LnurlStatus:
    authenticated: bool
    pubkey: Optional[str]
    token: Optional[str]
    raw: dict


class AuthResource(Resource):
    def create_challenge(self, pubkey: str) -> Challenge:
        """POST /auth/challenge — request a Nostr sign-in challenge."""
        if not isinstance(pubkey, str) or len(pubkey) != 64:
            raise MagmaError("pubkey must be a 64-char hex string")
        data = self._post("/auth/challenge", json_body={"pubkey": pubkey})
        return Challenge(
            challenge=str(data.get("challenge", "")),
            created_at=int(data.get("created_at", 0)),
        )

    def verify(self, signed_event: dict, challenge: str) -> AuthSession:
        """POST /auth/verify — exchange a signed event for a session token."""
        if not isinstance(signed_event, dict) or "pubkey" not in signed_event:
            raise MagmaError("signed_event must include a 'pubkey'")
        if not isinstance(challenge, str) or not challenge:
            raise MagmaError("challenge is required")
        data = self._post(
            "/auth/verify",
            json_body={"signed_event": signed_event, "challenge": challenge},
        )
        token = str(data.get("token", ""))
        pubkey = str(data.get("pubkey", ""))
        if not token or not pubkey:
            raise MagmaError("Server did not return a session token")
        session = AuthSession(token=token, pubkey=pubkey)
        # Auto-store the session on the client for convenience.
        self._client.set_token(token)
        return session

    def me(self) -> dict:
        """GET /auth/me — who am I, given the current token."""
        return self._get("/auth/me", auth=True)

    # ---- LNURL-auth flow ----

    def create_lnurl(self) -> LnurlChallenge:
        """POST /auth/lnurl — start an LNURL-auth challenge."""
        data = self._post("/auth/lnurl")
        if not isinstance(data, dict):
            raise MagmaError("Unexpected LNURL response")
        return LnurlChallenge(
            k1=str(data.get("k1", "")),
            lnurl=str(data.get("lnurl", "")),
            raw=data,
        )

    def lnurl_status(self, k1: str) -> LnurlStatus:
        """GET /auth/lnurl-status?k1=... — poll for wallet completion."""
        if not isinstance(k1, str) or not k1:
            raise MagmaError("k1 is required")
        data = self._get("/auth/lnurl-status", query={"k1": k1})
        if not isinstance(data, dict):
            raise MagmaError("Unexpected LNURL status response")
        token = data.get("token")
        pubkey = data.get("pubkey")
        authenticated = bool(token)
        if authenticated and isinstance(token, str):
            self._client.set_token(token)
        return LnurlStatus(
            authenticated=authenticated,
            pubkey=str(pubkey) if isinstance(pubkey, str) else None,
            token=str(token) if isinstance(token, str) else None,
            raw=data,
        )
