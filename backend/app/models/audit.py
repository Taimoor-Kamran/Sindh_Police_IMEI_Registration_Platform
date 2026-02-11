from datetime import datetime
from typing import Any, Optional

from sqlmodel import Column, Field, SQLModel
from sqlalchemy import JSON


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    action_type: str = Field(max_length=50, index=True)
    entity_type: Optional[str] = Field(default=None, max_length=50)
    entity_id: Optional[int] = Field(default=None)
    description: str
    extra_data: Optional[dict[str, Any]] = Field(default=None, sa_column=Column("metadata", JSON))
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class AuditLogRead(SQLModel):
    id: int
    user_id: Optional[int]
    action_type: str
    entity_type: Optional[str]
    entity_id: Optional[int]
    description: str
    extra_data: Optional[dict[str, Any]] = None
    ip_address: Optional[str]
    created_at: datetime
