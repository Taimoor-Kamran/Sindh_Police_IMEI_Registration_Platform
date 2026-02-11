from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select, func

from app.database import get_session
from app.models.audit import AuditLog, AuditLogRead
from app.models.mobile import Mobile, MobileRead
from app.models.police_alert import PoliceAlert, PoliceAlertRead
from app.models.snatch_report import SnatchReport, SnatchReportRead
from app.models.user import User, UserRead
from app.utils.rbac import require_role
from app.utils.audit import log_action

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _admin_user(current_user: User = Depends(require_role("police_admin"))) -> User:
    return current_user


@router.get("/shop-keepers", response_model=list[UserRead])
def list_shop_keepers(
    verified: bool | None = None,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    query = select(User).where(User.role == "shop_keeper")
    if verified is not None:
        query = query.where(User.is_shop_verified == verified)
    shops = session.exec(query).all()
    return shops


@router.put("/shop-keepers/{user_id}/approve", response_model=UserRead)
def approve_shop_keeper(
    user_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user or user.role != "shop_keeper":
        raise HTTPException(status_code=404, detail="Shop keeper not found")

    user.is_shop_verified = True
    user.updated_at = datetime.utcnow()
    session.add(user)

    log_action(
        session,
        action_type="SHOP_APPROVED",
        description=f"Shop keeper {user.username} (ID {user.id}) approved by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="user",
        entity_id=user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(user)
    return user


@router.put("/shop-keepers/{user_id}/suspend", response_model=UserRead)
def suspend_shop_keeper(
    user_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user or user.role != "shop_keeper":
        raise HTTPException(status_code=404, detail="Shop keeper not found")

    user.is_shop_verified = False
    user.is_active = False
    user.updated_at = datetime.utcnow()
    session.add(user)

    log_action(
        session,
        action_type="SHOP_SUSPENDED",
        description=f"Shop keeper {user.username} (ID {user.id}) suspended by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="user",
        entity_id=user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(user)
    return user


@router.get("/search-imei/{imei}", response_model=MobileRead)
def search_imei(
    imei: str,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    device = session.exec(select(Mobile).where(Mobile.imei == imei)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/mobiles/{device_id}/block", response_model=MobileRead)
def block_device(
    device_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    device = session.get(Mobile, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.status = "blocked"
    device.updated_at = datetime.utcnow()
    session.add(device)

    log_action(
        session,
        action_type="DEVICE_BLOCKED",
        description=f"Device {device.imei} blocked by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(device)
    return device


@router.put("/mobiles/{device_id}/unblock", response_model=MobileRead)
def unblock_device(
    device_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    device = session.get(Mobile, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.status = "active"
    device.updated_at = datetime.utcnow()
    session.add(device)

    log_action(
        session,
        action_type="DEVICE_UNBLOCKED",
        description=f"Device {device.imei} unblocked by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="mobile",
        entity_id=device.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(device)
    return device


@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_audit_logs(
    action_type: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    query = select(AuditLog).order_by(AuditLog.created_at.desc())
    if action_type:
        query = query.where(AuditLog.action_type == action_type)
    query = query.offset(offset).limit(limit)
    logs = session.exec(query).all()
    return logs


@router.get("/alerts", response_model=list[PoliceAlertRead])
def list_alerts(
    is_reviewed: bool | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    query = select(PoliceAlert).order_by(PoliceAlert.created_at.desc())
    if is_reviewed is not None:
        query = query.where(PoliceAlert.is_reviewed == is_reviewed)
    query = query.offset(offset).limit(limit)
    alerts = session.exec(query).all()
    return alerts


@router.put("/alerts/{alert_id}/review", response_model=PoliceAlertRead)
def review_alert(
    alert_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    alert = session.get(PoliceAlert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_reviewed = True
    session.add(alert)

    log_action(
        session,
        action_type="ALERT_REVIEWED",
        description=f"Alert #{alert.id} for IMEI {alert.imei} reviewed by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="police_alert",
        entity_id=alert.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(alert)
    return alert


@router.get("/snatch-reports", response_model=list[SnatchReportRead])
def list_snatch_reports(
    is_reviewed: bool | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    query = select(SnatchReport).order_by(SnatchReport.created_at.desc())
    if is_reviewed is not None:
        query = query.where(SnatchReport.is_reviewed == is_reviewed)
    query = query.offset(offset).limit(limit)
    reports = session.exec(query).all()
    return reports


@router.put("/snatch-reports/{report_id}/review", response_model=SnatchReportRead)
def review_snatch_report(
    report_id: int,
    request: Request,
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    report = session.get(SnatchReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.is_reviewed = True
    report.status = "under_review"
    report.reviewed_by_user_id = current_user.id
    report.reviewed_at = datetime.utcnow()
    session.add(report)

    log_action(
        session,
        action_type="SNATCH_REPORT_REVIEWED",
        description=f"Snatch report #{report.id} for IMEI {report.device_imei} reviewed by admin {current_user.username}",
        user_id=current_user.id,
        entity_type="snatch_report",
        entity_id=report.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    session.commit()
    session.refresh(report)
    return report


@router.get("/stats")
def admin_stats(
    current_user: User = Depends(_admin_user),
    session: Session = Depends(get_session),
):
    total_users = session.exec(select(func.count(User.id))).one()
    total_devices = session.exec(select(func.count(Mobile.id))).one()
    total_shops = session.exec(
        select(func.count(User.id)).where(User.role == "shop_keeper")
    ).one()
    pending_shops = session.exec(
        select(func.count(User.id)).where(
            User.role == "shop_keeper", User.is_shop_verified == False
        )
    ).one()
    blocked_devices = session.exec(
        select(func.count(Mobile.id)).where(Mobile.status == "blocked")
    ).one()
    unreviewed_alerts = session.exec(
        select(func.count(PoliceAlert.id)).where(PoliceAlert.is_reviewed == False)
    ).one()
    unreviewed_snatch_reports = session.exec(
        select(func.count(SnatchReport.id)).where(SnatchReport.is_reviewed == False)
    ).one()
    return {
        "total_users": total_users,
        "total_devices": total_devices,
        "total_shop_keepers": total_shops,
        "pending_shop_approvals": pending_shops,
        "blocked_devices": blocked_devices,
        "unreviewed_alerts": unreviewed_alerts,
        "unreviewed_snatch_reports": unreviewed_snatch_reports,
    }
