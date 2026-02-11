from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from app.database import get_session
from app.models.mobile import Mobile
from app.models.snatch_report import SnatchReport, SnatchReportCreate, SnatchReportRead
from app.models.user import User
from app.routes.auth import get_current_user
from app.utils.audit import log_action
from app.utils.validators import validate_cnic

router = APIRouter(prefix="/api/snatch-reports", tags=["snatch-reports"])


@router.post("", response_model=SnatchReportRead)
def create_snatch_report(
    data: SnatchReportCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Submit a snatching report. Auto-marks device as stolen if found in DB."""
    if not validate_cnic(data.victim_cnic):
        raise HTTPException(status_code=422, detail="Invalid CNIC format. Must be XXXXX-XXXXXXX-X")

    if not data.device_imei or len(data.device_imei) != 15 or not data.device_imei.isdigit():
        raise HTTPException(status_code=422, detail="IMEI must be exactly 15 digits")

    if not data.incident_description or len(data.incident_description.strip()) < 10:
        raise HTTPException(status_code=422, detail="Incident description must be at least 10 characters")

    # Check if device exists in system
    device = session.exec(select(Mobile).where(Mobile.imei == data.device_imei)).first()
    mobile_id = None

    if device:
        mobile_id = device.id
        # Auto-mark as stolen
        if device.status == "active":
            device.status = "stolen"
            device.updated_at = datetime.utcnow()
            session.add(device)

    incident_date = None
    if data.incident_date:
        try:
            incident_date = datetime.fromisoformat(data.incident_date)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format")

    ip = request.client.host if request.client else None
    report = SnatchReport(
        reporter_user_id=current_user.id,
        reporter_cnic=current_user.cnic,
        reporter_name=current_user.full_name,
        reporter_phone=current_user.mobile,
        victim_cnic=data.victim_cnic,
        device_imei=data.device_imei,
        mobile_id=mobile_id,
        incident_description=data.incident_description.strip(),
        incident_date=incident_date,
        incident_location=data.incident_location,
        ip_address=ip,
        user_agent=request.headers.get("user-agent"),
    )
    session.add(report)

    log_action(
        session,
        action_type="SNATCH_REPORT_FILED",
        description=f"Snatching report filed by {current_user.username} for IMEI {data.device_imei}, victim CNIC {data.victim_cnic}",
        user_id=current_user.id,
        entity_type="snatch_report",
        entity_id=None,
        ip_address=ip,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(report)
    return report


@router.get("", response_model=list[SnatchReportRead])
def list_my_reports(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List snatching reports submitted by the current user."""
    reports = session.exec(
        select(SnatchReport)
        .where(SnatchReport.reporter_user_id == current_user.id)
        .order_by(SnatchReport.created_at.desc())
    ).all()
    return reports


@router.get("/{report_id}", response_model=SnatchReportRead)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a specific report. Only the reporter or admin can view."""
    report = session.get(SnatchReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.reporter_user_id != current_user.id and current_user.role != "police_admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return report
