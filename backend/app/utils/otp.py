import random
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlmodel import Session, select, or_

from app.models.otp import OTP
from app.models.user import User

OTP_TTL_MINUTES = 5


def generate_otp_code() -> str:
    """Generate a random 6-digit OTP code."""
    return "".join(random.choices(string.digits, k=6))


def send_otp(
    session: Session,
    user: User,
    purpose: str,
    related_imei: str,
    ip_address: Optional[str] = None,
) -> OTP:
    """Create an OTP record and simulate sending it (console log for demo)."""
    code = generate_otp_code()
    otp = OTP(
        user_id=user.id,
        otp_code=code,
        purpose=purpose,
        related_imei=related_imei,
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_TTL_MINUTES),
        ip_address=ip_address,
    )
    session.add(otp)
    session.flush()

    # Simulated SMS — replace with real SMS gateway in production
    print(f"\n{'='*50}")
    print(f"[SIMULATED OTP] To: {user.full_name} ({user.mobile})")
    print(f"[SIMULATED OTP] Purpose: {purpose}")
    print(f"[SIMULATED OTP] IMEI: {related_imei}")
    print(f"[SIMULATED OTP] Code: {code}")
    print(f"[SIMULATED OTP] Expires in {OTP_TTL_MINUTES} minutes")
    print(f"{'='*50}\n")

    return otp


def verify_otp(
    session: Session,
    user_id: int,
    otp_code: str,
    purpose: str,
    related_imei: str,
) -> Tuple[bool, str]:
    """Verify an OTP code. Returns (success, error_message)."""
    otp = session.exec(
        select(OTP).where(
            OTP.user_id == user_id,
            OTP.purpose == purpose,
            OTP.related_imei == related_imei,
            OTP.is_used == False,
        ).order_by(OTP.created_at.desc())
    ).first()

    if not otp:
        return False, "No OTP found for this operation"

    if otp.expires_at < datetime.utcnow():
        return False, "OTP has expired. Please request a new one."

    if otp.otp_code != otp_code:
        return False, "Invalid OTP code"

    # Mark as used
    otp.is_used = True
    otp.verified_at = datetime.utcnow()
    session.add(otp)

    return True, ""


def find_user_by_identifier(session: Session, identifier: str) -> Optional[User]:
    """Look up a user by CNIC first, then by mobile number."""
    user = session.exec(
        select(User).where(
            or_(User.cnic == identifier, User.mobile == identifier)
        )
    ).first()
    return user
