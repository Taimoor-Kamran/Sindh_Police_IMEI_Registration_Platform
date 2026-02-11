from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OTP(SQLModel, table=True):
    __tablename__ = "otps"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    otp_code: str = Field(max_length=6)
    purpose: str = Field(max_length=50)  # TRANSFER_OLD_OWNER / TRANSFER_NEW_OWNER
    related_imei: str = Field(max_length=15, index=True)
    is_used: bool = Field(default=False)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    verified_at: Optional[datetime] = Field(default=None)
    ip_address: Optional[str] = Field(default=None, max_length=45)
