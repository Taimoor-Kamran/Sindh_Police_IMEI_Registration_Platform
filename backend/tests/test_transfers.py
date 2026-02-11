"""Tests for transfer history endpoints (GET only - POST moved to device-check)."""


def test_list_transfers_empty(client, auth_header):
    """List transfers returns empty when no transfers exist."""
    resp = client.get("/api/transfers", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_transfers_after_device_check_transfer(client, auth_header, sample_mobile_data):
    """Transfer history shows records created via device-check/transfer."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    # Create buyer
    buyer_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    resp = client.post("/api/auth/register", json=buyer_data)
    buyer_header = {"Authorization": f"Bearer {resp.json()['token']}"}

    # Transfer via new device-check flow
    client.post(
        "/api/device-check/transfer",
        json={"imei": sample_mobile_data["imei"], "transfer_type": "SALE", "notes": "Sold"},
        headers=buyer_header,
    )

    # Buyer should see the transfer in history
    resp = client.get("/api/transfers", headers=buyer_header)
    assert resp.status_code == 200
    transfers = resp.json()
    assert len(transfers) == 1
    assert transfers[0]["new_owner_cnic"] == "55555-6666666-7"
    assert transfers[0]["transfer_type"] == "SALE"


def test_get_transfer_by_id(client, auth_header, sample_mobile_data):
    """Can retrieve a specific transfer record by ID."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    buyer_data = {
        "full_name": "Buyer User",
        "cnic": "55555-6666666-7",
        "mobile": "03201234567",
        "email": "buyer@example.com",
        "username": "buyeruser",
        "password": "BuyerPass123",
    }
    resp = client.post("/api/auth/register", json=buyer_data)
    buyer_header = {"Authorization": f"Bearer {resp.json()['token']}"}

    client.post(
        "/api/device-check/transfer",
        json={"imei": sample_mobile_data["imei"], "transfer_type": "GIFT"},
        headers=buyer_header,
    )

    # Get transfer list first
    resp = client.get("/api/transfers", headers=buyer_header)
    transfer_id = resp.json()[0]["id"]

    # Get by ID
    resp = client.get(f"/api/transfers/{transfer_id}", headers=buyer_header)
    assert resp.status_code == 200
    assert resp.json()["transfer_type"] == "GIFT"


def test_old_post_transfer_removed(client, auth_header, sample_mobile_data):
    """The old POST /api/transfers endpoint should no longer exist."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.post(
        "/api/transfers",
        json={
            "imei": sample_mobile_data["imei"],
            "new_owner_cnic": "55555-6666666-7",
            "transfer_type": "SALE",
        },
        headers=auth_header,
    )
    assert resp.status_code == 405  # Method Not Allowed
