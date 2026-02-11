"""Tests for data visibility / isolation restrictions."""


SAMPLE_IMEI = "490154203237518"
SAMPLE_IMEI_2 = "353456789012276"  # Luhn-valid


def test_citizen_only_sees_owned_devices(client, auth_header, sample_mobile_data):
    """Citizens only see devices where current_owner_cnic matches their CNIC."""
    # Register device as citizen (owner = citizen's CNIC)
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    # Create second user
    second_user = {
        "full_name": "Other User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "other@example.com",
        "username": "otheruser",
        "password": "OtherPass123",
    }
    resp = client.post("/api/auth/register", json=second_user)
    other_header = {"Authorization": f"Bearer {resp.json()['token']}"}

    # Other user should see zero devices (not the owner)
    resp = client.get("/api/mobiles", headers=other_header)
    assert resp.status_code == 200
    assert len(resp.json()) == 0

    # Original citizen should see their device
    resp = client.get("/api/mobiles", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_shop_only_sees_owned_devices(client, shop_header, admin_header, sample_mobile_data):
    """Shop keepers only see devices they OWN (by CNIC), not just registered."""
    # Shop registers device for a customer (customer is owner, not shop)
    resp = client.post(
        "/api/mobiles/register-shop",
        json={
            "imei": sample_mobile_data["imei"],
            "mobile_number": sample_mobile_data["mobile_number"],
            "brand": "Samsung",
            "model": "Galaxy S24",
            "customer_cnic": "77777-8888888-9",
        },
        headers=shop_header,
    )
    assert resp.status_code == 200

    # Shop should NOT see this device in their list (they don't own it)
    resp = client.get("/api/mobiles", headers=shop_header)
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_by_imei_denied_for_non_owner(client, auth_header, sample_mobile_data):
    """Non-owner, non-registerer, non-admin cannot access by-imei."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    # Create second user
    second_user = {
        "full_name": "Other User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "other@example.com",
        "username": "otheruser",
        "password": "OtherPass123",
    }
    resp = client.post("/api/auth/register", json=second_user)
    other_header = {"Authorization": f"Bearer {resp.json()['token']}"}

    resp = client.get(f"/api/mobiles/by-imei/{sample_mobile_data['imei']}", headers=other_header)
    assert resp.status_code == 403


def test_by_imei_allowed_for_admin(client, auth_header, admin_header, sample_mobile_data):
    """Admin can access any device by IMEI."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.get(f"/api/mobiles/by-imei/{sample_mobile_data['imei']}", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["imei"] == sample_mobile_data["imei"]


def test_by_imei_allowed_for_owner(client, auth_header, sample_mobile_data):
    """Device owner can access by IMEI."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.get(f"/api/mobiles/by-imei/{sample_mobile_data['imei']}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["imei"] == sample_mobile_data["imei"]
