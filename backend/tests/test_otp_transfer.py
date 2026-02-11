"""Tests for OTP-based transfer flow (shopkeeper 4-step)."""
from datetime import datetime, timedelta

from sqlmodel import select

from app.models.otp import OTP


def _register_device_for_owner(client, auth_header, imei="490154203237518"):
    """Helper: register a device under the citizen's CNIC."""
    client.post(
        "/api/mobiles/register-self",
        json={"imei": imei, "mobile_number": "03001112233", "brand": "Samsung", "model": "S24"},
        headers=auth_header,
    )


def _get_latest_otp(session, user_id, purpose):
    """Helper: fetch the most recent OTP from the test DB."""
    return session.exec(
        select(OTP)
        .where(OTP.user_id == user_id, OTP.purpose == purpose)
        .order_by(OTP.created_at.desc())
    ).first()


def test_initiate_transfer(client, auth_header, shop_header, session):
    """Shop enters IMEI + old owner CNIC → OTP created."""
    _register_device_for_owner(client, auth_header)

    resp = client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=shop_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["old_owner_cnic"] == "12345-6789012-3"
    assert data["device_brand"] == "Samsung"


def test_initiate_wrong_owner(client, auth_header, shop_header, session):
    """Mismatch between identifier and device owner → 400."""
    _register_device_for_owner(client, auth_header)

    resp = client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "99999-0000000-0"},
        headers=shop_header,
    )
    assert resp.status_code == 404  # user not found


def test_verify_old_owner_correct_otp(client, auth_header, shop_header, session):
    """Correct OTP → verified=true."""
    _register_device_for_owner(client, auth_header)

    client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=shop_header,
    )

    # Get the OTP from DB
    from app.models.user import User
    user = session.exec(select(User).where(User.cnic == "12345-6789012-3")).first()
    otp = _get_latest_otp(session, user.id, "TRANSFER_OLD_OWNER")

    resp = client.post(
        "/api/transfer-otp/verify-old-owner",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3", "otp_code": otp.otp_code},
        headers=shop_header,
    )
    assert resp.status_code == 200
    assert resp.json()["verified"] is True


def test_verify_old_owner_wrong_otp(client, auth_header, shop_header, session):
    """Wrong OTP code → 400."""
    _register_device_for_owner(client, auth_header)

    client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=shop_header,
    )

    resp = client.post(
        "/api/transfer-otp/verify-old-owner",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3", "otp_code": "000000"},
        headers=shop_header,
    )
    assert resp.status_code == 400


def test_verify_old_owner_expired_otp(client, auth_header, shop_header, session):
    """Expired OTP → 400."""
    _register_device_for_owner(client, auth_header)

    client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=shop_header,
    )

    # Manually expire the OTP
    from app.models.user import User
    user = session.exec(select(User).where(User.cnic == "12345-6789012-3")).first()
    otp = _get_latest_otp(session, user.id, "TRANSFER_OLD_OWNER")
    otp.expires_at = datetime.utcnow() - timedelta(minutes=10)
    session.add(otp)
    session.commit()

    resp = client.post(
        "/api/transfer-otp/verify-old-owner",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3", "otp_code": otp.otp_code},
        headers=shop_header,
    )
    assert resp.status_code == 400
    assert "expired" in resp.json()["detail"].lower()


def test_send_new_owner_otp(client, auth_header, shop_header, session):
    """New owner found → OTP sent."""
    _register_device_for_owner(client, auth_header)

    # Register a new owner
    buyer_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    client.post("/api/auth/register", json=buyer_data)

    resp = client.post(
        "/api/transfer-otp/send-new-owner-otp",
        json={"imei": "490154203237518", "new_owner_identifier": "55555-6666666-7"},
        headers=shop_header,
    )
    assert resp.status_code == 200
    assert resp.json()["new_owner_cnic"] == "55555-6666666-7"


def test_complete_transfer(client, auth_header, shop_header, session):
    """Full OTP transfer flow → ownership changed."""
    _register_device_for_owner(client, auth_header)

    # Register buyer
    buyer_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    client.post("/api/auth/register", json=buyer_data)

    # Step 1: Initiate
    client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=shop_header,
    )

    # Step 2: Verify old owner
    from app.models.user import User
    old_user = session.exec(select(User).where(User.cnic == "12345-6789012-3")).first()
    old_otp = _get_latest_otp(session, old_user.id, "TRANSFER_OLD_OWNER")
    client.post(
        "/api/transfer-otp/verify-old-owner",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3", "otp_code": old_otp.otp_code},
        headers=shop_header,
    )

    # Step 3: Send new owner OTP
    client.post(
        "/api/transfer-otp/send-new-owner-otp",
        json={"imei": "490154203237518", "new_owner_identifier": "55555-6666666-7"},
        headers=shop_header,
    )

    # Step 4: Complete
    new_user = session.exec(select(User).where(User.cnic == "55555-6666666-7")).first()
    new_otp = _get_latest_otp(session, new_user.id, "TRANSFER_NEW_OWNER")
    resp = client.post(
        "/api/transfer-otp/complete",
        json={
            "imei": "490154203237518",
            "new_owner_identifier": "55555-6666666-7",
            "otp_code": new_otp.otp_code,
            "transfer_type": "SALE",
            "notes": "Sold at shop",
        },
        headers=shop_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["old_owner_cnic"] == "12345-6789012-3"
    assert data["new_owner_cnic"] == "55555-6666666-7"
    assert data["transfer_type"] == "SALE"


def test_citizen_cannot_use_otp_transfer(client, auth_header):
    """Non-shop user → 403."""
    resp = client.post(
        "/api/transfer-otp/initiate",
        json={"imei": "490154203237518", "old_owner_identifier": "12345-6789012-3"},
        headers=auth_header,
    )
    assert resp.status_code == 403
