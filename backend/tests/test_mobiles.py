def test_citizen_register_device(client, auth_header, sample_mobile_data):
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["imei"] == sample_mobile_data["imei"]
    assert data["registration_type"] == "SELF"
    assert data["status"] == "active"


def test_register_invalid_imei(client, auth_header):
    resp = client.post(
        "/api/mobiles/register-self",
        json={"imei": "123456789012345", "mobile_number": "03001112233"},
        headers=auth_header,
    )
    assert resp.status_code == 422


def test_register_duplicate_imei(client, auth_header, sample_mobile_data):
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    assert resp.status_code == 409


def test_list_devices(client, auth_header, sample_mobile_data):
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.get("/api/mobiles", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_device_by_id(client, auth_header, sample_mobile_data):
    reg = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = reg.json()["id"]
    resp = client.get(f"/api/mobiles/{device_id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["imei"] == sample_mobile_data["imei"]


def test_get_device_by_imei(client, auth_header, sample_mobile_data):
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.get(f"/api/mobiles/by-imei/{sample_mobile_data['imei']}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["brand"] == "Samsung"


def test_get_stats(client, auth_header, sample_mobile_data):
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.get("/api/mobiles/stats", headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["owned_devices"] == 1
    assert data["registered_devices"] == 1


def test_shop_register_device(client, shop_header):
    resp = client.post(
        "/api/mobiles/register-shop",
        json={
            "imei": "490154203237518",
            "mobile_number": "03001112233",
            "brand": "Apple",
            "model": "iPhone 15",
            "customer_cnic": "55555-6666666-7",
        },
        headers=shop_header,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["registration_type"] == "SHOP"
    assert data["current_owner_cnic"] == "55555-6666666-7"


def test_unverified_shop_cannot_register(client, shop_keeper_data):
    """Unverified shop keeper should be rejected."""
    # Register shop but don't approve
    reg = client.post("/api/auth/register-shop", json=shop_keeper_data)
    token = reg.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/api/mobiles/register-shop",
        json={
            "imei": "490154203237518",
            "mobile_number": "03001112233",
            "customer_cnic": "55555-6666666-7",
        },
        headers=headers,
    )
    assert resp.status_code == 403


def test_unauthenticated_register(client, sample_mobile_data):
    resp = client.post("/api/mobiles/register-self", json=sample_mobile_data)
    assert resp.status_code == 401
