from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from app.database import get_session
from app.models.mobile import Mobile, MobileRead
from app.models.ownership import OwnershipHistory, TransferRead
from app.models.user import User
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


# ── Citizen endpoints ──


@router.get("/citizen/my-devices", response_model=list[MobileRead])
def citizen_my_devices(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Devices where current_owner_cnic matches the user's CNIC."""
    devices = session.exec(
        select(Mobile).where(Mobile.current_owner_cnic == current_user.cnic)
    ).all()
    return devices


@router.get("/citizen/my-transfers", response_model=list[TransferRead])
def citizen_my_transfers(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Transfers where old or new owner matches user's CNIC."""
    transfers = session.exec(
        select(OwnershipHistory).where(
            (OwnershipHistory.old_owner_cnic == current_user.cnic)
            | (OwnershipHistory.new_owner_cnic == current_user.cnic)
        ).order_by(OwnershipHistory.transfer_date.desc())
    ).all()
    return transfers


@router.get("/citizen/stats")
def citizen_stats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    total_owned = session.exec(
        select(func.count(Mobile.id)).where(Mobile.current_owner_cnic == current_user.cnic)
    ).one()
    total_transferred_away = session.exec(
        select(func.count(OwnershipHistory.id)).where(
            OwnershipHistory.old_owner_cnic == current_user.cnic
        )
    ).one()
    total_received = session.exec(
        select(func.count(OwnershipHistory.id)).where(
            OwnershipHistory.new_owner_cnic == current_user.cnic
        )
    ).one()
    return {
        "total_owned": total_owned,
        "total_transferred_away": total_transferred_away,
        "total_received": total_received,
    }


# ── Shop endpoints ──


@router.get("/shop/registered-devices", response_model=list[MobileRead])
def shop_registered_devices(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Devices registered by this shop keeper (registration_type = SHOP)."""
    devices = session.exec(
        select(Mobile).where(
            Mobile.registered_by_user_id == current_user.id,
            Mobile.registration_type == "SHOP",
        )
    ).all()
    return devices


@router.get("/shop/transfers-performed", response_model=list[TransferRead])
def shop_transfers_performed(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Transfers performed by this user (transferred_by_user_id = user.id)."""
    transfers = session.exec(
        select(OwnershipHistory).where(
            OwnershipHistory.transferred_by_user_id == current_user.id
        ).order_by(OwnershipHistory.transfer_date.desc())
    ).all()
    return transfers


@router.get("/shop/stats")
def shop_stats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    total_registered = session.exec(
        select(func.count(Mobile.id)).where(
            Mobile.registered_by_user_id == current_user.id,
            Mobile.registration_type == "SHOP",
        )
    ).one()
    total_transferred = session.exec(
        select(func.count(OwnershipHistory.id)).where(
            OwnershipHistory.transferred_by_user_id == current_user.id
        )
    ).one()
    return {
        "total_registered": total_registered,
        "total_transferred": total_transferred,
    }
