from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.user import User, UserRead
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserRead)
def update_profile(
    full_name: str | None = None,
    email: str | None = None,
    mobile: str | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if full_name is not None:
        current_user.full_name = full_name
    if email is not None:
        current_user.email = email
    if mobile is not None:
        current_user.mobile = mobile
    current_user.updated_at = datetime.utcnow()

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
