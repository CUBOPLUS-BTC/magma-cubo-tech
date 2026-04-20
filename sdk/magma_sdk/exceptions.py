"""Custom exceptions raised by the Magma SDK."""

from __future__ import annotations

from typing import Any, Optional


class MagmaError(Exception):
    """Base class for all Magma SDK errors."""


class TransportError(MagmaError):
    """The request could not be dispatched or completed.

    Raised for connection failures, timeouts, DNS errors, TLS errors, or
    responses that are not valid JSON.
    """


class APIError(MagmaError):
    """The server returned a non-success HTTP status.

    Attributes:
        status: The HTTP status code.
        detail: The ``detail`` field from the error body when present.
        response: The decoded JSON body (``dict`` if possible, else ``str``).
    """

    def __init__(
        self,
        status: int,
        detail: Optional[str] = None,
        response: Any = None,
        message: Optional[str] = None,
    ) -> None:
        self.status = status
        self.detail = detail
        self.response = response
        super().__init__(message or detail or f"HTTP {status}")


class ValidationError(APIError):
    """HTTP 400 — request body failed server-side validation."""


class AuthenticationError(APIError):
    """HTTP 401 — missing or invalid credentials."""


class PermissionError_(APIError):
    """HTTP 403 — authenticated but not permitted."""


class NotFoundError(APIError):
    """HTTP 404 — resource not found."""


class RateLimitError(APIError):
    """HTTP 429 — caller is being rate limited."""


class ServerError(APIError):
    """HTTP 5xx — upstream failure."""


_STATUS_TO_ERROR = {
    400: ValidationError,
    401: AuthenticationError,
    403: PermissionError_,
    404: NotFoundError,
    429: RateLimitError,
}


def api_error_for(status: int, detail: Optional[str], body: Any) -> APIError:
    """Return the most specific :class:`APIError` subclass for ``status``."""
    if 500 <= status < 600:
        return ServerError(status=status, detail=detail, response=body)
    cls = _STATUS_TO_ERROR.get(status, APIError)
    return cls(status=status, detail=detail, response=body)
