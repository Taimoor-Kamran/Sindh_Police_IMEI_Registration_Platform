def test_register_shop_keeper(client, shop_keeper_data):
    resp = client.post("/api/auth/register-shop", json=shop_keeper_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "token" in data


def test_register_shop_invalid_license(client, shop_keeper_data):
    shop_keeper_data["shop_license_number"] = "ab"  # too short
    resp = client.post("/api/auth/register-shop", json=shop_keeper_data)
    assert resp.status_code == 422


def test_list_shop_keepers(client, admin_header, shop_keeper_data):
    client.post("/api/auth/register-shop", json=shop_keeper_data)
    resp = client.get("/api/admin/shop-keepers", headers=admin_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_approve_shop_keeper(client, admin_header, shop_keeper_data):
    reg = client.post("/api/auth/register-shop", json=shop_keeper_data)
    user_id = reg.json()["user_id"]

    resp = client.put(f"/api/admin/shop-keepers/{user_id}/approve", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["is_shop_verified"] is True


def test_suspend_shop_keeper(client, admin_header, shop_keeper_data):
    reg = client.post("/api/auth/register-shop", json=shop_keeper_data)
    user_id = reg.json()["user_id"]

    resp = client.put(f"/api/admin/shop-keepers/{user_id}/suspend", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["is_shop_verified"] is False
    assert resp.json()["is_active"] is False


def test_admin_search_imei(client, admin_header, auth_header, sample_mobile_data):
    # Citizen registers device
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    # Admin searches
    resp = client.get(f"/api/admin/search-imei/{sample_mobile_data['imei']}", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["imei"] == sample_mobile_data["imei"]


def test_admin_block_device(client, admin_header, auth_header, sample_mobile_data):
    reg = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = reg.json()["id"]

    resp = client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["status"] == "blocked"


def test_admin_unblock_device(client, admin_header, auth_header, sample_mobile_data):
    reg = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = reg.json()["id"]

    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)
    resp = client.put(f"/api/admin/mobiles/{device_id}/unblock", headers=admin_header)
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"


def test_admin_audit_logs(client, admin_header, auth_header, sample_mobile_data):
    # Create some activity
    client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    resp = client.get("/api/admin/audit-logs", headers=admin_header)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_admin_stats(client, admin_header):
    resp = client.get("/api/admin/stats", headers=admin_header)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_users" in data
    assert "total_devices" in data
    assert "total_shop_keepers" in data


def test_citizen_cannot_access_admin(client, auth_header):
    resp = client.get("/api/admin/shop-keepers", headers=auth_header)
    assert resp.status_code == 403


def test_cannot_transfer_blocked_device(client, admin_header, auth_header, sample_mobile_data):
    reg = client.post("/api/mobiles/register-self", json=sample_mobile_data, headers=auth_header)
    device_id = reg.json()["id"]

    # Block the device
    client.put(f"/api/admin/mobiles/{device_id}/block", headers=admin_header)

    # Try to transfer via device-check flow
    resp = client.post(
        "/api/device-check/transfer",
        json={
            "imei": sample_mobile_data["imei"],
            "transfer_type": "SALE",
        },
        headers=auth_header,
    )
    assert resp.status_code == 400
