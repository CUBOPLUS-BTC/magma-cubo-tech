"""HTTP transport used by the SDK.

Stdlib-only (``urllib.request``) to avoid pulling in a dependency on
``requests``. Supports per-request timeout, bounded retries with
exponential backoff on transient failures (connection / 5xx / 429),
bearer-token auth, and structured error decoding.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional

from .exceptions import TransportError, api_error_for


DEFAULT_USER_AGENT = "magma-sdk-python/0.1.0"
_RETRIABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}


@dataclass(frozen=True)
class TransportConfig:
    base_url: str
    timeout: float = 10.0
    max_retries: int = 2
    backoff: float = 0.25
    user_agent: str = DEFAULT_USER_AGENT


class HTTPTransport:
    """Thin wrapper around :mod:`urllib.request` with retries and errors."""

    def __init__(
        self,
        config: TransportConfig,
        *,
        opener: Optional[Callable[..., Any]] = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._config = config
        self._opener = opener or urllib.request.urlopen
        self._sleep = sleep

    @property
    def base_url(self) -> str:
        return self._config.base_url

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        query: Optional[Mapping[str, Any]] = None,
        token: Optional[str] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        url = self._build_url(path, query)
        data: Optional[bytes] = None
        headers = {
            "Accept": "application/json",
            "User-Agent": self._config.user_agent,
        }
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if extra_headers:
            headers.update(extra_headers)

        req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)

        attempt = 0
        while True:
            attempt += 1
            try:
                with self._opener(req, timeout=self._config.timeout) as response:
                    status = getattr(response, "status", None) or response.getcode()
                    raw = response.read()
                body = self._decode(raw)
                if 200 <= status < 300:
                    return body
                # Non-2xx with a JSON body.
                if status in _RETRIABLE_STATUS and attempt <= self._config.max_retries:
                    self._sleep(self._config.backoff * (2 ** (attempt - 1)))
                    continue
                detail = body.get("detail") if isinstance(body, dict) else None
                raise api_error_for(status, detail, body)
            except urllib.error.HTTPError as exc:
                raw = exc.read() if hasattr(exc, "read") else b""
                body = self._decode(raw)
                status = exc.code
                if status in _RETRIABLE_STATUS and attempt <= self._config.max_retries:
                    self._sleep(self._config.backoff * (2 ** (attempt - 1)))
                    continue
                detail = body.get("detail") if isinstance(body, dict) else None
                raise api_error_for(status, detail, body) from None
            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
                if attempt <= self._config.max_retries:
                    self._sleep(self._config.backoff * (2 ** (attempt - 1)))
                    continue
                raise TransportError(f"Request to {url} failed: {exc}") from exc

    def _build_url(self, path: str, query: Optional[Mapping[str, Any]]) -> str:
        base = self._config.base_url.rstrip("/")
        if not path.startswith("/"):
            path = "/" + path
        url = f"{base}{path}"
        if query:
            cleaned = {k: v for k, v in query.items() if v is not None}
            if cleaned:
                url = f"{url}?{urllib.parse.urlencode(cleaned)}"
        return url

    @staticmethod
    def _decode(raw: bytes) -> Any:
        if not raw:
            return None
        try:
            return json.loads(raw.decode("utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            raise TransportError("Server returned non-JSON response") from exc
