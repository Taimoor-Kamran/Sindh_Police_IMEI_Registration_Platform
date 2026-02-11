from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.ownership import OwnershipHistory, TransferRead
from app.models.user import User
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/transfers", tags=["transfers"])


@router.get("", response_model=list[TransferRead])
def list_transfers(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transfers = session.exec(
        select(OwnershipHistory).where(
            (OwnershipHistory.old_owner_cnic == current_user.cnic)
            | (OwnershipHistory.new_owner_cnic == current_user.cnic)
            | (OwnershipHistory.transferred_by_user_id == current_user.id)
        )
    ).all()
    return transfers


@router.get("/{transfer_id}", response_model=TransferRead)
def get_transfer(
    transfer_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    transfer = session.get(OwnershipHistory, transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")

    # Only involved parties can view
    is_involved = (
        transfer.old_owner_cnic == current_user.cnic
        or transfer.new_owner_cnic == current_user.cnic
        or transfer.transferred_by_user_id == current_user.id
        or current_user.role == "police_admin"
    )
    if not is_involved:
        raise HTTPException(status_code=403, detail="Access denied")

    return transfer
