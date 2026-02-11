from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from app.config import settings
from app.database import get_session
from app.models.user import User, UserCreate, UserLogin, ShopKeeperCreate, Session as UserSession
from app.utils.security import (
    create_access_token,
    hash_password,
    hash_token,
    verify_password,
    verify_token,
)
from app.utils.validators import validate_cnic, validate_mobile, validate_password, validate_username

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = session.get(User, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user


def _check_duplicate_user(session: Session, user_data) -> None:
    existing = session.exec(
        select(User).where(
            (User.username == user_data.username)
            | (User.cnic == user_data.cnic)
            | (User.email == user_data.email)
            | (User.mobile == user_data.mobile)
        )
    ).first()

    if existing:
        if existing.username == user_data.username:
            raise HTTPException(status_code=409, detail="Username already exists")
        if existing.cnic == user_data.cnic:
            raise HTTPException(status_code=409, detail="CNIC already registered")
        if existing.email == user_data.email:
            raise HTTPException(status_code=409, detail="Email already registered")
        if existing.mobile == user_data.mobile:
            raise HTTPException(status_code=409, detail="Mobile number already registered")


def _validate_common_fields(user_data) -> None:
    if not validate_cnic(user_data.cnic):
        raise HTTPException(status_code=422, detail="CNIC must be in format XXXXX-XXXXXXX-X")
    if not validate_mobile(user_data.mobile):
        raise HTTPException(status_code=422, detail="Mobile must start with 03 and be 11 digits")
    pw_err = validate_password(user_data.password)
    if pw_err:
        raise HTTPException(status_code=422, detail=pw_err)
    un_err = validate_username(user_data.username)
    if un_err:
        raise HTTPException(status_code=422, detail=un_err)


def _create_session_token(user: User, request: Request, session: Session) -> str:
    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
    })
    user_session = UserSession(
        user_id=user.id,
        token_hash=hash_token(token),
        expires_at=datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    session.add(user_session)
    session.commit()
    return token


@router.post("/register")
def register(user_data: UserCreate, request: Request, session: Session = Depends(get_session)):
    _validate_common_fields(user_data)
    _check_duplicate_user(session, user_data)

    user = User(
        full_name=user_data.full_name,
        cnic=user_data.cnic,
        mobile=user_data.mobile,
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = _create_session_token(user, request, session)

    return {
        "success": True,
        "message": "Registration successful",
        "user_id": user.id,
        "token": token,
    }


@router.post("/register-shop")
def register_shop(user_data: ShopKeeperCreate, request: Request, session: Session = Depends(get_session)):
    _validate_common_fields(user_data)

    if not user_data.shop_license_number or len(user_data.shop_license_number.strip()) < 3:
        raise HTTPException(status_code=422, detail="Shop license number is required (min 3 characters)")

    _check_duplicate_user(session, user_data)

    user = User(
        full_name=user_data.full_name,
        cnic=user_data.cnic,
        mobile=user_data.mobile,
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        role="shop_keeper",
        shop_license_number=user_data.shop_license_number.strip(),
        is_shop_verified=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = _create_session_token(user, request, session)

    return {
        "success": True,
        "message": "Shop keeper registration successful. Awaiting police admin verification.",
        "user_id": user.id,
        "token": token,
    }


@router.post("/login")
def login(credentials: UserLogin, request: Request, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == credentials.username)).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = _create_session_token(user, request, session)

    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_shop_verified": user.is_shop_verified,
        },
    }


@router.post("/logout")
def logout(request: Request, session: Session = Depends(get_session)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.split(" ")[1]
    token_h = hash_token(token)

    db_session = session.exec(select(UserSession).where(UserSession.token_hash == token_h)).first()
    if db_session:
        session.delete(db_session)
        session.commit()

    return {"success": True, "message": "Logged out successfully"}


@router.get("/verify")
def verify(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "is_shop_verified": current_user.is_shop_verified,
        },
    }
