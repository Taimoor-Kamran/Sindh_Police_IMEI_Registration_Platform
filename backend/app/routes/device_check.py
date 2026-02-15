from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.mobile import Mobile
from app.models.ownership import OwnershipHistory
from app.models.police_alert import PoliceAlert
from app.models.user import User
from app.routes.auth import get_current_user
from app.utils.validators import validate_imei
from app.utils.audit import log_action

router = APIRouter(prefix="/api/device-check", tags=["device-check"])

VALID_TRANSFER_TYPES = {"SALE", "GIFT", "INHERITANCE", "OTHER"}


class DeviceCheckRequest(BaseModel):
    imei: str


class DeviceCheckResponse(BaseModel):
    found: bool
    status: str
    brand: Optional[str] = None
    model: Optional[str] = None
    registration_date: Optional[str] = None
    message: Optional[str] = None
    is_owner: bool = False


class DeviceTransferRequest(BaseModel):
    imei: str
    transfer_type: str
    notes: Optional[str] = None


class DeviceTransferOutRequest(BaseModel):
    imei: str
    new_owner_cnic: str
    transfer_type: str
    notes: Optional[str] = None


@router.post("", response_model=DeviceCheckResponse)
def check_device(
    data: DeviceCheckRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Check IMEI status. If stolen/blocked, creates a police alert."""
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

    device = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()

    if not device:
        return DeviceCheckResponse(found=False, status="not_registered")

    if device.status == "active":
        return DeviceCheckResponse(
            found=True,
            status="active",
            brand=device.brand,
            model=device.model,
            registration_date=device.registration_date.isoformat(),
            is_owner=device.current_owner_cnic == current_user.cnic,
        )

    # Device is stolen or blocked - create police alert
    alert = PoliceAlert(
        imei=data.imei,
        mobile_id=device.id,
        checker_user_id=current_user.id,
        checker_cnic=current_user.cnic,
        checker_name=current_user.full_name,
        checker_phone=current_user.mobile,
        checker_role=current_user.role,
        device_status=device.status,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    session.add(alert)

    log_action(
        session,
        action_type="STOLEN_DEVICE_CHECKED",
        description=f"Stolen/blocked device {data.imei} checked by {current_user.username} (CNIC: {current_user.cnic})",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()

    return DeviceCheckResponse(
        found=True,
        status=device.status,
        message="This device is reported as stolen/blocked. Police have been alerted with your details.",
    )


@router.post("/transfer")
def transfer_device(
    data: DeviceTransferRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Transfer a clean device to the current user's CNIC."""
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

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

    if device.current_owner_cnic == current_user.cnic:
        raise HTTPException(status_code=400, detail="You already own this device")

    old_cnic = device.current_owner_cnic

    # Create ownership history record
    transfer = OwnershipHistory(
        mobile_id=device.id,
        imei=device.imei,
        old_owner_cnic=old_cnic,
        new_owner_cnic=current_user.cnic,
        transferred_by_user_id=current_user.id,
        transfer_type=data.transfer_type,
        notes=data.notes,
    )
    session.add(transfer)

    # Update device ownership
    device.current_owner_cnic = current_user.cnic
    session.add(device)

    log_action(
        session,
        action_type="DEVICE_TRANSFERRED",
        description=f"Device {data.imei} transferred from {old_cnic} to {current_user.cnic}",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(device)

    return {
        "message": "Device transferred successfully",
        "imei": device.imei,
        "new_owner_cnic": device.current_owner_cnic,
        "brand": device.brand,
        "model": device.model,
    }


@router.post("/transfer-out")
def transfer_device_out(
    data: DeviceTransferOutRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Owner transfers their device to a new buyer by CNIC."""
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

    if data.transfer_type not in VALID_TRANSFER_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Transfer type must be one of: {', '.join(sorted(VALID_TRANSFER_TYPES))}",
        )

    from app.utils.validators import validate_cnic
    if not validate_cnic(data.new_owner_cnic):
        raise HTTPException(status_code=422, detail="New owner CNIC must be in format XXXXX-XXXXXXX-X")

    device = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if device.status != "active":
        raise HTTPException(status_code=400, detail=f"Cannot transfer device with status '{device.status}'")

    if device.current_owner_cnic != current_user.cnic:
        raise HTTPException(status_code=403, detail="You are not the owner of this device")

    if data.new_owner_cnic == current_user.cnic:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    old_cnic = device.current_owner_cnic

    transfer = OwnershipHistory(
        mobile_id=device.id,
        imei=device.imei,
        old_owner_cnic=old_cnic,
        new_owner_cnic=data.new_owner_cnic,
        transferred_by_user_id=current_user.id,
        transfer_type=data.transfer_type,
        notes=data.notes,
    )
    session.add(transfer)

    device.current_owner_cnic = data.new_owner_cnic
    session.add(device)

    log_action(
        session,
        action_type="DEVICE_TRANSFERRED_OUT",
        description=f"Device {data.imei} transferred by owner {current_user.cnic} to {data.new_owner_cnic}",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(device)

    return {
        "message": "Device transferred to new owner successfully",
        "imei": device.imei,
        "old_owner_cnic": old_cnic,
        "new_owner_cnic": data.new_owner_cnic,
        "brand": device.brand,
        "model": device.model,
    }
