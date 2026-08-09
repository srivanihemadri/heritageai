from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.dependencies import get_current_admin, get_current_user
from app.main import app
from app.models.user import UserRole


client = TestClient(app)


def test_users_me_requires_authentication():
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_normal_user_cannot_list_users():
    user = SimpleNamespace(
        id="user-1",
        full_name="Test User",
        email="user@example.com",
        role=UserRole.USER,
        is_active=True,
    )

    app.dependency_overrides[get_current_admin] = lambda: (_ for _ in ()).throw(
        __import__("app.core.exceptions", fromlist=["ForbiddenException"]).ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )
    )

    try:
        response = client.get("/api/v1/users")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_authenticated_user_can_get_own_profile():
    user = SimpleNamespace(
        id="user-1",
        full_name="Test User",
        email="user@example.com",
        role=UserRole.USER,
        is_active=True,
    )

    app.dependency_overrides[get_current_user] = lambda: user

    try:
        response = client.get("/api/v1/users/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "user-1"


def test_admin_can_list_users():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    app.dependency_overrides[get_current_admin] = lambda: admin

    class FakeQuery:
        def order_by(self, *args):
            return self

        def all(self):
            return [admin]

    class FakeDB:
        def query(self, *args):
            return FakeQuery()

    from app.db.session import get_db

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        response = client.get("/api/v1/users")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["total"] == 1
