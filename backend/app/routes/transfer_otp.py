from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.mobile import Mobile
from app.models.ownership import OwnershipHistory
from app.models.user import User
from app.utils.audit import log_action
from app.utils.otp import find_user_by_identifier, send_otp, verify_otp
from app.utils.rbac import require_verified_shop
from app.utils.validators import validate_imei

router = APIRouter(prefix="/api/transfer-otp", tags=["transfer-otp"])

VALID_TRANSFER_TYPES = {"SALE", "GIFT", "INHERITANCE", "OTHER"}


class InitiateRequest(BaseModel):
    imei: str
    old_owner_identifier: str


class VerifyOldOwnerRequest(BaseModel):
    imei: str
    old_owner_identifier: str
    otp_code: str


class SendNewOwnerOTPRequest(BaseModel):
    imei: str
    new_owner_identifier: str


class CompleteRequest(BaseModel):
    imei: str
    new_owner_identifier: str
    otp_code: str
    transfer_type: str
    notes: Optional[str] = None


@router.post("/initiate")
def initiate_transfer(
    data: InitiateRequest,
    request: Request,
    current_user: User = Depends(require_verified_shop),
    session: Session = Depends(get_session),
):
    """Step 1: Validate IMEI, find old owner, send OTP to old owner."""
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

    device = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found in system")
    if device.status != "active":
        raise HTTPException(status_code=400, detail=f"Cannot transfer device with status '{device.status}'")

    old_owner = find_user_by_identifier(session, data.old_owner_identifier)
    if not old_owner:
        raise HTTPException(status_code=404, detail="Old owner not found. They must be a registered user.")

    if device.current_owner_cnic != old_owner.cnic:
        raise HTTPException(status_code=400, detail="This person is not the current owner of this device")

    ip = request.client.host if request.client else None
    send_otp(session, old_owner, "TRANSFER_OLD_OWNER", data.imei, ip)
    session.commit()

    return {
        "message": "OTP sent to old owner for verification",
        "old_owner_cnic": old_owner.cnic,
        "old_owner_name": old_owner.full_name,
        "device_brand": device.brand,
        "device_model": device.model,
    }


@router.post("/verify-old-owner")
def verify_old_owner(
    data: VerifyOldOwnerRequest,
    request: Request,
    current_user: User = Depends(require_verified_shop),
    session: Session = Depends(get_session),
):
    """Step 2: Verify the old owner's OTP."""
    old_owner = find_user_by_identifier(session, data.old_owner_identifier)
    if not old_owner:
        raise HTTPException(status_code=404, detail="Old owner not found")

    success, error = verify_otp(session, old_owner.id, data.otp_code, "TRANSFER_OLD_OWNER", data.imei)
    if not success:
        raise HTTPException(status_code=400, detail=error)

    session.commit()

    return {"message": "Old owner verified successfully", "verified": True}


@router.post("/send-new-owner-otp")
def send_new_owner_otp(
    data: SendNewOwnerOTPRequest,
    request: Request,
    current_user: User = Depends(require_verified_shop),
    session: Session = Depends(get_session),
):
    """Step 3: Find new owner by CNIC/phone, send OTP."""
    device = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    new_owner = find_user_by_identifier(session, data.new_owner_identifier)
    if not new_owner:
        raise HTTPException(status_code=404, detail="New owner not found. They must be a registered user.")

    if device.current_owner_cnic == new_owner.cnic:
        raise HTTPException(status_code=400, detail="New owner is already the current owner of this device")

    ip = request.client.host if request.client else None
    send_otp(session, new_owner, "TRANSFER_NEW_OWNER", data.imei, ip)
    session.commit()

    return {
        "message": "OTP sent to new owner for verification",
        "new_owner_cnic": new_owner.cnic,
        "new_owner_name": new_owner.full_name,
    }


@router.post("/complete")
def complete_transfer(
    data: CompleteRequest,
    request: Request,
    current_user: User = Depends(require_verified_shop),
    session: Session = Depends(get_session),
):
    """Step 4: Verify new owner OTP, perform transfer."""
    if data.transfer_type not in VALID_TRANSFER_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Transfer type must be one of: {', '.join(sorted(VALID_TRANSFER_TYPES))}",
        )

    device = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if device.status != "active":
        raise HTTPException(status_code=400, detail=f"Cannot transfer device with status '{device.status}'")

    new_owner = find_user_by_identifier(session, data.new_owner_identifier)
    if not new_owner:
        raise HTTPException(status_code=404, detail="New owner not found")

    success, error = verify_otp(session, new_owner.id, data.otp_code, "TRANSFER_NEW_OWNER", data.imei)
    if not success:
        raise HTTPException(status_code=400, detail=error)

    old_cnic = device.current_owner_cnic

    # Create ownership history
    transfer = OwnershipHistory(
        mobile_id=device.id,
        imei=device.imei,
        old_owner_cnic=old_cnic,
        new_owner_cnic=new_owner.cnic,
        transferred_by_user_id=current_user.id,
        transfer_type=data.transfer_type,
        notes=data.notes,
    )
    session.add(transfer)

    # Update device ownership
    device.current_owner_cnic = new_owner.cnic
    session.add(device)

    ip = request.client.host if request.client else None
    log_action(
        session,
        action_type="OTP_TRANSFER_COMPLETED",
        description=f"OTP transfer: {data.imei} from {old_cnic} to {new_owner.cnic} by shop {current_user.username}",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=ip,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()

    return {
        "message": "Transfer completed successfully",
        "imei": data.imei,
        "old_owner_cnic": old_cnic,
        "new_owner_cnic": new_owner.cnic,
        "transfer_type": data.transfer_type,
    }
