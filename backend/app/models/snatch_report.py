from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SnatchReport(SQLModel, table=True):
    __tablename__ = "snatch_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    reporter_user_id: int = Field(foreign_key="users.id", index=True)
    reporter_cnic: str = Field(max_length=15)
    reporter_name: str = Field(max_length=255)
    reporter_phone: str = Field(max_length=15)
    victim_cnic: str = Field(max_length=15, index=True)
    device_imei: str = Field(max_length=15, index=True)
    mobile_id: Optional[int] = Field(default=None, foreign_key="mobiles.id")
    incident_description: str
    incident_date: Optional[datetime] = Field(default=None)
    incident_location: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="pending", max_length=20)  # pending/under_review/resolved
    is_reviewed: bool = Field(default=False)
    reviewed_by_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    reviewed_at: Optional[datetime] = Field(default=None)
    admin_notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)


class SnatchReportCreate(SQLModel):
    victim_cnic: str
    device_imei: str
    incident_description: str
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None


class SnatchReportRead(SQLModel):
    id: int
    reporter_user_id: int
    reporter_cnic: str
    reporter_name: str
    reporter_phone: str
    victim_cnic: str
    device_imei: str
    mobile_id: Optional[int]
    incident_description: str
    incident_date: Optional[datetime]
    incident_location: Optional[str]
    status: str
    is_reviewed: bool
    reviewed_by_user_id: Optional[int]
    reviewed_at: Optional[datetime]
    admin_notes: Optional[str]
    created_at: datetime
