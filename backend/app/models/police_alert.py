from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PoliceAlert(SQLModel, table=True):
    __tablename__ = "police_alerts"

    id: Optional[int] = Field(default=None, primary_key=True)
    imei: str = Field(max_length=15, index=True)
    mobile_id: Optional[int] = Field(default=None, foreign_key="mobiles.id")
    checker_user_id: int = Field(foreign_key="users.id")
    checker_cnic: str = Field(max_length=15)
    checker_name: str = Field(max_length=255)
    checker_phone: str = Field(max_length=15)
    checker_role: str = Field(max_length=20)
    device_status: str = Field(max_length=20)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
    is_reviewed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class PoliceAlertRead(SQLModel):
    id: int
    imei: str
    mobile_id: Optional[int]
    checker_user_id: int
    checker_cnic: str
    checker_name: str
    checker_phone: str
    checker_role: str
    device_status: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_reviewed: bool
    created_at: datetime
