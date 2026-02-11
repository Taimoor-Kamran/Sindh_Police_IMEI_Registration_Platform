def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "2.0.0"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_success(client, test_user_data):
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user_id"] is not None


def test_register_duplicate_username(client, test_user_data):
    client.post("/api/auth/register", json=test_user_data)
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 409


def test_register_invalid_cnic(client, test_user_data):
    test_user_data["cnic"] = "invalid"
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 422


def test_register_invalid_mobile(client, test_user_data):
    test_user_data["mobile"] = "1234567890"
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 422


def test_register_weak_password(client, test_user_data):
    test_user_data["password"] = "weak"
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 422


def test_login_success(client, test_user_data):
    client.post("/api/auth/register", json=test_user_data)
    response = client.post(
        "/api/auth/login",
        json={"username": test_user_data["username"], "password": test_user_data["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["username"] == test_user_data["username"]


def test_login_wrong_password(client, test_user_data):
    client.post("/api/auth/register", json=test_user_data)
    response = client.post(
        "/api/auth/login",
        json={"username": test_user_data["username"], "password": "WrongPass123"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "nobody", "password": "Pass1234"},
    )
    assert response.status_code == 401


def test_verify_token(client, test_user_data):
    reg = client.post("/api/auth/register", json=test_user_data)
    token = reg.json()["token"]
    response = client.get(
        "/api/auth/verify", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == test_user_data["username"]


def test_verify_invalid_token(client):
    response = client.get(
        "/api/auth/verify", headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401


def test_logout(client, test_user_data):
    reg = client.post("/api/auth/register", json=test_user_data)
    token = reg.json()["token"]
    response = client.post(
        "/api/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_profile(client, test_user_data):
    reg = client.post("/api/auth/register", json=test_user_data)
    token = reg.json()["token"]
    response = client.get(
        "/api/user/profile", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == test_user_data["full_name"]
    assert response.json()["username"] == test_user_data["username"]
