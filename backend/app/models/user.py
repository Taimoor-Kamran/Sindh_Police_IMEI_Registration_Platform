from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    full_name: str = Field(min_length=3, max_length=255)
    cnic: str = Field(max_length=15, unique=True, index=True)
    mobile: str = Field(max_length=15, unique=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(min_length=4, max_length=50, unique=True, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    role: str = Field(default="citizen", max_length=20)
    shop_license_number: Optional[str] = Field(default=None, max_length=50)
    is_shop_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    full_name: str
    cnic: str
    mobile: str
    email: str
    username: str
    password: str


class ShopKeeperCreate(SQLModel):
    full_name: str
    cnic: str
    mobile: str
    email: str
    username: str
    password: str
    shop_license_number: str


class UserRead(SQLModel):
    id: int
    full_name: str
    cnic: str
    mobile: str
    email: str
    username: str
    role: str
    shop_license_number: Optional[str] = None
    is_shop_verified: bool = False
    created_at: datetime
    is_active: bool


class UserLogin(SQLModel):
    username: str
    password: str


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    token_hash: str = Field(max_length=255)
    expires_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None)
