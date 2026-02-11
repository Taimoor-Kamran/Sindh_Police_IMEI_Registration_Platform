import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app
from app.models.user import User
from app.utils.security import hash_password


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    return {
        "full_name": "Test User",
        "cnic": "12345-6789012-3",
        "mobile": "03001234567",
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123",
    }


@pytest.fixture
def shop_keeper_data():
    return {
        "full_name": "Shop Owner",
        "cnic": "11111-2222222-3",
        "mobile": "03111234567",
        "email": "shop@example.com",
        "username": "shopowner",
        "password": "ShopPass123",
        "shop_license_number": "SL-2024-001",
    }


@pytest.fixture
def auth_header(client, test_user_data):
    """Register a citizen user and return auth header."""
    resp = client.post("/api/auth/register", json=test_user_data)
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_user(session):
    """Create a police_admin user directly in the DB and return (user, token)."""
    from app.utils.security import create_access_token

    user = User(
        full_name="Police Admin",
        cnic="99999-9999999-9",
        mobile="03009999999",
        email="admin@test.com",
        username="policeadmin",
        password_hash=hash_password("Admin@123456"),
        role="police_admin",
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return user, token


@pytest.fixture
def admin_header(admin_user):
    """Return auth header for admin user."""
    _, token = admin_user
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def verified_shop_user(client, session, shop_keeper_data, admin_header):
    """Register a shop keeper and approve them via admin. Return (user_data, token)."""
    resp = client.post("/api/auth/register-shop", json=shop_keeper_data)
    data = resp.json()
    token = data["token"]
    user_id = data["user_id"]

    # Admin approves
    client.put(f"/api/admin/shop-keepers/{user_id}/approve", headers=admin_header)

    return shop_keeper_data, token


@pytest.fixture
def shop_header(verified_shop_user):
    """Return auth header for verified shop keeper."""
    _, token = verified_shop_user
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_mobile_data():
    return {
        "imei": "490154203237518",
        "mobile_number": "03001112233",
        "brand": "Samsung",
        "model": "Galaxy S24",
    }
