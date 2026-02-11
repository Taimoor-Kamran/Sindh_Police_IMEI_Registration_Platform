from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select, func, extract

from app.config import settings
from app.database import get_session
from app.models.mobile import Mobile, MobileCreate, MobileShopCreate, MobileRead
from app.models.user import User
from app.routes.auth import get_current_user
from app.utils.rbac import require_role, require_verified_shop
from app.utils.validators import validate_imei, validate_cnic
from app.utils.audit import log_action

router = APIRouter(prefix="/api/mobiles", tags=["mobiles"])


@router.post("/register-self", response_model=MobileRead)
def register_self(
    data: MobileCreate,
    request: Request,
    current_user: User = Depends(require_role("citizen", "shop_keeper")),
    session: Session = Depends(get_session),
):
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

    # Check duplicate IMEI
    existing = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Device with this IMEI is already registered")

    # Check citizen registration limit
    current_year = datetime.utcnow().year
    count = session.exec(
        select(func.count(Mobile.id)).where(
            Mobile.registered_by_user_id == current_user.id,
            Mobile.registration_type == "SELF",
            extract("year", Mobile.registration_date) == current_year,
        )
    ).one()
    if count >= settings.max_citizen_registrations_per_year:
        raise HTTPException(
            status_code=429,
            detail=f"Registration limit reached ({settings.max_citizen_registrations_per_year} per year)",
        )

    mobile = Mobile(
        imei=data.imei,
        mobile_number=data.mobile_number,
        brand=data.brand,
        model=data.model,
        current_owner_cnic=current_user.cnic,
        registered_by_user_id=current_user.id,
        registration_type="SELF",
        notes=data.notes,
    )
    session.add(mobile)

    log_action(
        session,
        action_type="DEVICE_REGISTERED",
        description=f"Device {data.imei} registered by citizen {current_user.username}",
        user_id=current_user.id,
        entity_type="mobile",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(mobile)
    return mobile


@router.post("/register-shop", response_model=MobileRead)
def register_shop(
    data: MobileShopCreate,
    request: Request,
    current_user: User = Depends(require_verified_shop),
    session: Session = Depends(get_session),
):
    if not validate_imei(data.imei):
        raise HTTPException(status_code=422, detail="Invalid IMEI. Must be 15 digits and pass Luhn check")

    if not validate_cnic(data.customer_cnic):
        raise HTTPException(status_code=422, detail="Customer CNIC must be in format XXXXX-XXXXXXX-X")

    # Check duplicate IMEI
    existing = session.exec(select(Mobile).where(Mobile.imei == data.imei)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Device with this IMEI is already registered")

    # Check shop daily limit
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    count = session.exec(
        select(func.count(Mobile.id)).where(
            Mobile.registered_by_user_id == current_user.id,
            Mobile.registration_type == "SHOP",
            Mobile.registration_date >= today_start,
        )
    ).one()
    if count >= settings.max_shop_registrations_per_day:
        raise HTTPException(
            status_code=429,
            detail=f"Daily registration limit reached ({settings.max_shop_registrations_per_day} per day)",
        )

    mobile = Mobile(
        imei=data.imei,
        mobile_number=data.mobile_number,
        brand=data.brand,
        model=data.model,
        current_owner_cnic=data.customer_cnic,
        registered_by_user_id=current_user.id,
        registration_type="SHOP",
        notes=data.notes,
    )
    session.add(mobile)

    log_action(
        session,
        action_type="DEVICE_REGISTERED_SHOP",
        description=f"Device {data.imei} registered by shop {current_user.username} for CNIC {data.customer_cnic}",
        user_id=current_user.id,
        entity_type="mobile",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(mobile)
    return mobile


@router.get("", response_model=list[MobileRead])
def list_mobiles(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List devices owned by the current user (by CNIC). Admins see all."""
    if current_user.role == "police_admin":
        devices = session.exec(select(Mobile)).all()
    else:
        devices = session.exec(
            select(Mobile).where(Mobile.current_owner_cnic == current_user.cnic)
        ).all()
    return devices


@router.get("/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    owned = session.exec(
        select(func.count(Mobile.id)).where(Mobile.current_owner_cnic == current_user.cnic)
    ).one()
    registered = session.exec(
        select(func.count(Mobile.id)).where(Mobile.registered_by_user_id == current_user.id)
    ).one()
    stolen = session.exec(
        select(func.count(Mobile.id)).where(
            Mobile.current_owner_cnic == current_user.cnic,
            Mobile.status == "stolen",
        )
    ).one()
    return {
        "owned_devices": owned,
        "registered_devices": registered,
        "stolen_devices": stolen,
    }


@router.get("/by-imei/{imei}", response_model=MobileRead)
def get_by_imei(
    imei: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    device = session.exec(select(Mobile).where(Mobile.imei == imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    # Only owner, registerer, or admin can view
    if (
        device.current_owner_cnic != current_user.cnic
        and device.registered_by_user_id != current_user.id
        and current_user.role != "police_admin"
    ):
        raise HTTPException(status_code=403, detail="Access denied")
    return device


@router.get("/{device_id}", response_model=MobileRead)
def get_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    device = session.get(Mobile, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    # Only owner or the user who registered it can see details
    if device.current_owner_cnic != current_user.cnic and device.registered_by_user_id != current_user.id and current_user.role != "police_admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return device
