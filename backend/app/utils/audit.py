from typing import Any

from sqlmodel import Session

from app.models.audit import AuditLog


def log_action(
    session: Session,
    action_type: str,
    description: str,
    user_id: int | None = None,
    entity_type: str | None = None,
    entity_id: int | None = None,
    extra_data: dict[str, Any] | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> AuditLog:
    """Insert an audit log record."""
    log = AuditLog(
        user_id=user_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        extra_data=extra_data,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    session.add(log)
    return log
