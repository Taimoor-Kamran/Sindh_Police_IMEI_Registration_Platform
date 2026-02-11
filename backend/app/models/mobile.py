from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Mobile(SQLModel, table=True):
    __tablename__ = "mobiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    imei: str = Field(max_length=15, unique=True, index=True)
    mobile_number: str = Field(max_length=15)
    brand: Optional[str] = Field(default=None, max_length=100)
    model: Optional[str] = Field(default=None, max_length=100)
    current_owner_cnic: str = Field(max_length=15, index=True)
    registered_by_user_id: int = Field(foreign_key="users.id", index=True)
    registration_type: str = Field(max_length=10)  # "SHOP" or "SELF"
    status: str = Field(default="active", max_length=20)  # active/stolen/blocked
    invoice_path: Optional[str] = Field(default=None, max_length=500)
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None)


class MobileCreate(SQLModel):
    """Citizen self-registration: CNIC auto-filled from user."""
    imei: str
    mobile_number: str
    brand: Optional[str] = None
    model: Optional[str] = None
    notes: Optional[str] = None


class MobileShopCreate(SQLModel):
    """Shop keeper registers device for a customer."""
    imei: str
    mobile_number: str
    brand: Optional[str] = None
    model: Optional[str] = None
    customer_cnic: str
    notes: Optional[str] = None


class MobileRead(SQLModel):
    id: int
    imei: str
    mobile_number: str
    brand: Optional[str]
    model: Optional[str]
    current_owner_cnic: str
    registered_by_user_id: int
    registration_type: str
    status: str
    invoice_path: Optional[str]
    registration_date: datetime
    updated_at: datetime
    notes: Optional[str]
