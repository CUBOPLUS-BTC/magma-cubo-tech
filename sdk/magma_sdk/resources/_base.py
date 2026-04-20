"""Shared base class for resource clients."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Optional

if TYPE_CHECKING:
    from ..client import MagmaClient


class Resource:
    """Attach a resource to a :class:`MagmaClient` instance."""

    def __init__(self, client: "MagmaClient") -> None:
        self._client = client

    def _get(
        self,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        auth: bool = False,
        request_id: Optional[str] = None,
    ) -> Any:
        return self._client._request(
            "GET", path, query=query, auth=auth, request_id=request_id
        )

    def _post(
        self,
        path: str,
        *,
        json_body: Any = None,
        query: Optional[Mapping[str, Any]] = None,
        auth: bool = False,
        idempotency_key: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> Any:
        return self._client._request(
            "POST",
            path,
            json_body=json_body,
            query=query,
            auth=auth,
            idempotency_key=idempotency_key,
            request_id=request_id,
        )
