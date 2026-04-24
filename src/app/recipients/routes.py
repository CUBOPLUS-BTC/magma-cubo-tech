"""HTTP route handlers for recipients.

Each handler returns ``(body_dict, status_code)`` to match the project
convention used across the other modules.
"""

from __future__ import annotations

from .manager import RecipientsManager

_manager = RecipientsManager()


def handle_list_recipients(pubkey: str) -> tuple[dict, int]:
    """GET /recipients — list recipients for the authenticated user."""
    if not pubkey:
        return {"detail": "Authentication required"}, 401
    try:
        rows = _manager.list_for_user(pubkey)
        return {"recipients": rows, "total": len(rows)}, 200
    except Exception as exc:
        return {"detail": f"No se pudieron listar destinatarios: {exc}"}, 500


def handle_create_recipient(body: dict, pubkey: str) -> tuple[dict, int]:
    """POST /recipients — create a recipient for the authenticated user."""
    if not pubkey:
        return {"detail": "Authentication required"}, 401
    if not isinstance(body, dict):
        return {"detail": "Cuerpo inválido"}, 400

    name = body.get("name", "")
    lightning_address = body.get("lightning_address", "")
    country = body.get("country", "SV")
    amount = body.get("default_amount_usd")
    skip = bool(body.get("skip_lnurl_check", False))

    try:
        recipient = _manager.create(
            pubkey=pubkey,
            name=name,
            lightning_address=lightning_address,
            country=country,
            default_amount_usd=amount,
            skip_lnurl_check=skip,
        )
        return {"recipient": recipient, "message": "Destinatario creado"}, 201
    except ValueError as exc:
        return {"detail": str(exc)}, 422
    except Exception as exc:
        return {"detail": f"Error al crear destinatario: {exc}"}, 500


def handle_get_recipient(recipient_id: int, pubkey: str) -> tuple[dict, int]:
    """GET /recipients/:id — fetch a single recipient."""
    if not pubkey:
        return {"detail": "Authentication required"}, 401
    try:
        return {"recipient": _manager.get(recipient_id, pubkey)}, 200
    except KeyError as exc:
        return {"detail": str(exc)}, 404
    except Exception as exc:
        return {"detail": f"Error al consultar destinatario: {exc}"}, 500


def handle_update_recipient(
    recipient_id: int, body: dict, pubkey: str
) -> tuple[dict, int]:
    """PATCH /recipients/:id — partial update."""
    if not pubkey:
        return {"detail": "Authentication required"}, 401
    if not isinstance(body, dict) or not body:
        return {"detail": "Cuerpo vacío"}, 400
    try:
        updated = _manager.update(recipient_id, pubkey, body)
        return {"recipient": updated, "message": "Destinatario actualizado"}, 200
    except KeyError as exc:
        return {"detail": str(exc)}, 404
    except ValueError as exc:
        return {"detail": str(exc)}, 422
    except Exception as exc:
        return {"detail": f"Error al actualizar: {exc}"}, 500


def handle_delete_recipient(
    recipient_id: int, pubkey: str
) -> tuple[dict, int]:
    """DELETE /recipients/:id — delete a recipient."""
    if not pubkey:
        return {"detail": "Authentication required"}, 401
    try:
        removed = _manager.delete(recipient_id, pubkey)
        if not removed:
            return {"detail": "Destinatario no encontrado"}, 404
        return {"message": "Destinatario eliminado", "id": recipient_id}, 200
    except Exception as exc:
        return {"detail": f"Error al eliminar: {exc}"}, 500
