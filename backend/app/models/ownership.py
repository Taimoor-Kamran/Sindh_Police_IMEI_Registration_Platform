from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OwnershipHistory(SQLModel, table=True):
    __tablename__ = "ownership_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    mobile_id: int = Field(foreign_key="mobiles.id", index=True)
    imei: str = Field(max_length=15, index=True)
    old_owner_cnic: str = Field(max_length=15, index=True)
    new_owner_cnic: str = Field(max_length=15, index=True)
    transferred_by_user_id: int = Field(foreign_key="users.id")
    transfer_type: str = Field(max_length=20)  # SALE/GIFT/INHERITANCE/OTHER
    transfer_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None)


class TransferCreate(SQLModel):
    imei: str
    new_owner_cnic: str
    transfer_type: str  # SALE/GIFT/INHERITANCE/OTHER
    notes: Optional[str] = None


class TransferRead(SQLModel):
    id: int
    mobile_id: int
    imei: str
    old_owner_cnic: str
    new_owner_cnic: str
    transferred_by_user_id: int
    transfer_type: str
    transfer_date: datetime
    notes: Optional[str]
