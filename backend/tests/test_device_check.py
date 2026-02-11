"""Tests for the device check and transfer flow."""


def _register_device(client, auth_header, imei="490154203237518"):
    """Helper to register a device for the test citizen user."""
    return client.post(
        "/api/mobiles/register-self",
        json={
            "imei": imei,
            "mobile_number": "03001112233",
            "brand": "Samsung",
            "model": "Galaxy S24",
        },
        headers=auth_header,
    )


def _make_stolen(client, admin_header, device_id):
    """Helper to block a device (simulates stolen)."""
    return client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)


def test_check_active_device(client, auth_header, sample_mobile_data):
    """Checking an active device returns status without owner CNIC."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.post(
        "/api/device-check",
        json={"imei": sample_mobile_data["imei"]},
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["found"] is True
    assert data["status"] == "active"
    assert data["brand"] == "Samsung"
    assert data["model"] == "Galaxy S24"
    assert data.get("registration_date") is not None
    # Must NOT contain owner CNIC
    assert "current_owner_cnic" not in data


def test_check_stolen_device_creates_alert(client, auth_header, admin_header, sample_mobile_data):
    """Checking a stolen device creates a police alert."""
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = resp.json()["id"]

    # Block the device (simulates stolen)
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)

    resp = client.post(
        "/api/device-check",
        json={"imei": sample_mobile_data["imei"]},
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["found"] is True
    assert data["status"] == "blocked"
    assert "alerted" in data["message"].lower() or "police" in data["message"].lower()


def test_check_nonexistent_imei(client, auth_header):
    """Checking a non-registered IMEI returns not_registered."""
    resp = client.post(
        "/api/device-check",
        json={"imei": "490154203237518"},
        headers=auth_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["found"] is False
    assert data["status"] == "not_registered"


def test_check_invalid_imei(client, auth_header):
    """Checking an invalid IMEI returns 422."""
    resp = client.post(
        "/api/device-check",
        json={"imei": "12345"},
        headers=auth_header,
    )
    assert resp.status_code == 422


def test_transfer_active_device(client, auth_header, sample_mobile_data):
    """Transfer an active device to a new user."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    # Create a second user to receive the transfer
    second_user_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    resp = client.post("/api/auth/register", json=second_user_data)
    buyer_token = resp.json()["token"]
    buyer_header = {"Authorization": f"Bearer {buyer_token}"}

    resp = client.post(
        "/api/device-check/transfer",
        json={
            "imei": sample_mobile_data["imei"],
            "transfer_type": "SALE",
            "notes": "Purchased from seller",
        },
        headers=buyer_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["new_owner_cnic"] == "55555-6666666-7"
    assert data["imei"] == sample_mobile_data["imei"]


def test_transfer_stolen_device_blocked(client, auth_header, admin_header, sample_mobile_data):
    """Cannot transfer a stolen/blocked device."""
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = resp.json()["id"]
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)

    # Second user tries to transfer
    second_user_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    resp = client.post("/api/auth/register", json=second_user_data)
    buyer_header = {"Authorization": f"Bearer {resp.json()['token']}"}

    resp = client.post(
        "/api/device-check/transfer",
        json={"imei": sample_mobile_data["imei"], "transfer_type": "SALE"},
        headers=buyer_header,
    )
    assert resp.status_code == 400


def test_transfer_to_same_owner(client, auth_header, sample_mobile_data):
    """Cannot transfer a device to yourself."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.post(
        "/api/device-check/transfer",
        json={"imei": sample_mobile_data["imei"], "transfer_type": "SALE"},
        headers=auth_header,
    )
    assert resp.status_code == 400


def test_transfer_nonexistent_device(client, auth_header):
    """Transferring a non-existent IMEI returns 404."""
    resp = client.post(
        "/api/device-check/transfer",
        json={"imei": "490154203237518", "transfer_type": "SALE"},
        headers=auth_header,
    )
    assert resp.status_code == 404


def test_police_alert_has_full_details(client, auth_header, admin_header, sample_mobile_data, session):
    """Police alert contains checker's full details."""
    from app.models.police_alert import PoliceAlert

    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = resp.json()["id"]
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)

    client.post(
        "/api/device-check",
        json={"imei": sample_mobile_data["imei"]},
        headers=auth_header,
    )

    from sqlmodel import select
    alert = session.exec(select(PoliceAlert)).first()
    assert alert is not None
    assert alert.checker_cnic == "12345-6789012-3"
    assert alert.checker_name == "Test User"
    assert alert.checker_phone == "03001234567"
    assert alert.checker_role == "citizen"
    assert alert.device_status == "blocked"
    assert alert.is_reviewed is False


def test_admin_list_alerts(client, auth_header, admin_header, sample_mobile_data):
    """Admin can list police alerts."""
    # Create an alert by checking a blocked device
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = resp.json()["id"]
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)
    client.post(
        "/api/device-check",
        json={"imei": sample_mobile_data["imei"]},
        headers=auth_header,
    )

    resp = client.get("/api/admin/alerts", headers=admin_header)
    assert resp.status_code == 200
    alerts = resp.json()
    assert len(alerts) >= 1
    assert alerts[0]["imei"] == sample_mobile_data["imei"]


def test_admin_review_alert(client, auth_header, admin_header, sample_mobile_data):
    """Admin can mark an alert as reviewed."""
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = resp.json()["id"]
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)
    client.post(
        "/api/device-check",
        json={"imei": sample_mobile_data["imei"]},
        headers=auth_header,
    )

    # Get alerts
    alerts_resp = client.get("/api/admin/alerts", headers=admin_header)
    alert_id = alerts_resp.json()[0]["id"]

    resp = client.put(f"/api/admin/alerts/{alert_id}/review", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["is_reviewed"] is True


def test_citizen_cannot_see_alerts(client, auth_header):
    """Non-admin users cannot access alerts endpoint."""
    resp = client.get("/api/admin/alerts", headers=auth_header)
    assert resp.status_code == 403
