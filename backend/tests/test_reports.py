"""Tests for citizen/shop activity report endpoints."""


def test_citizen_stats(client, auth_header, sample_mobile_data):
    """Citizen stats returns correct counts."""
    # Register a device
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.get("/api/reports/citizen/stats", headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_owned"] == 1
    assert data["total_transferred_away"] == 0
    assert data["total_received"] == 0


def test_citizen_my_devices(client, auth_header, sample_mobile_data):
    """Only devices owned by this citizen are returned."""
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)

    resp = client.get("/api/reports/citizen/my-devices", headers=auth_header)
    assert resp.status_code == 200
    devices = resp.json()
    assert len(devices) == 1
    assert devices[0]["imei"] == sample_mobile_data["imei"]


def test_shop_registered_devices(client, shop_header, session):
    """Only SHOP-type devices registered by this user are returned."""
    # Register a device as shop
    client.post(
        "/api/mobiles/register-shop",
        json={
            "imei": "490154203237518",
            "mobile_number": "03001112233",
            "brand": "Samsung",
            "model": "Galaxy S24",
            "customer_cnic": "55555-6666666-7",
        },
        headers=shop_header,
    )

    resp = client.get("/api/reports/shop/registered-devices", headers=shop_header)
    assert resp.status_code == 200
    devices = resp.json()
    assert len(devices) == 1
    assert devices[0]["registration_type"] == "SHOP"


def test_shop_stats(client, shop_header):
    """Shop stats returns correct counts."""
    # Register a device
    client.post(
        "/api/mobiles/register-shop",
        json={
            "imei": "490154203237518",
            "mobile_number": "03001112233",
            "brand": "Samsung",
            "model": "Galaxy S24",
            "customer_cnic": "55555-6666666-7",
        },
        headers=shop_header,
    )

    resp = client.get("/api/reports/shop/stats", headers=shop_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_registered"] == 1
    assert data["total_transferred"] == 0
