from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole


client = TestClient(app)


def test_heritage_sites_list_is_public():
    class FakeQuery:
        def filter(self, *args):
            return self

        def with_entities(self, *args):
            return self

        def scalar(self):
            return 0

        def order_by(self, *args):
            return self

        def offset(self, *args):
            return self

        def limit(self, *args):
            return self

        def all(self):
            return []

    class FakeDB:
        def query(self, *args):
            return FakeQuery()

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        response = client.get("/api/v1/heritage-sites")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["sites"] == []
    assert response.json()["data"]["total"] == 0
    assert response.json()["data"]["page"] == 1
    assert response.json()["data"]["page_size"] == 20
    assert response.json()["data"]["total_pages"] == 0


def test_normal_user_cannot_create_heritage_site():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites",
            json={
                "name": "Test Heritage Site",
                "slug": "test-heritage-site",
                "category": "Monument",
                "country": "India",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_create_site(db, data):
        return SimpleNamespace(
            id="site-1",
            name=data.name,
            slug=data.slug,
            short_description=data.short_description,
            description=data.description,
            category=data.category,
            country=data.country,
            state=data.state,
            city=data.city,
            latitude=data.latitude,
            longitude=data.longitude,
            established_year=data.established_year,
            architectural_style=data.architectural_style,
            historical_period=data.historical_period,
            significance=data.significance,
            preservation_status=data.preservation_status,
            is_verified=False,
            is_active=True,
        )

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create_site = heritage_sites.create_site
    heritage_sites.create_site = fake_create_site

    try:
        response = client.post(
            "/api/v1/heritage-sites",
            json={
                "name": "Test Heritage Site",
                "slug": "test-heritage-site",
                "category": "Monument",
                "country": "India",
            },
        )
    finally:
        heritage_sites.create_site = original_create_site
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "site-1"


def test_admin_can_update_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_update_site(db, site_id, data):
        return SimpleNamespace(
            id=site_id,
            name=data.name or "Existing Site",
            slug=data.slug or "existing-site",
            short_description=None,
            description=None,
            category=data.category or "Monument",
            country=data.country or "India",
            state=None,
            city=None,
            latitude=None,
            longitude=None,
            established_year=None,
            architectural_style=None,
            historical_period=None,
            significance=None,
            preservation_status=None,
            is_verified=False,
            is_active=True,
        )

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_update_site = heritage_sites.update_site
    heritage_sites.update_site = fake_update_site

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1",
            json={
                "name": "Updated Heritage Site",
            },
        )
    finally:
        heritage_sites.update_site = original_update_site
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "Updated Heritage Site"


def test_admin_can_delete_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    deleted = {"value": False}

    def fake_delete_site(db, site_id):
        deleted["value"] = True

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_delete_site = heritage_sites.delete_site
    heritage_sites.delete_site = fake_delete_site

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1",
        )
    finally:
        heritage_sites.delete_site = original_delete_site
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["value"] is True

def test_normal_user_cannot_verify_heritage_site():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/verify",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_verify_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_verify_site(db, site_id):
        return SimpleNamespace(
            id=site_id,
            name="Test Heritage Site",
            slug="test-heritage-site",
            short_description=None,
            description=None,
            category="Monument",
            country="India",
            state=None,
            city=None,
            latitude=None,
            longitude=None,
            established_year=None,
            architectural_style=None,
            historical_period=None,
            significance=None,
            preservation_status=None,
            is_verified=True,
            is_active=True,
        )

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_verify_site = heritage_sites.verify_site
    heritage_sites.verify_site = fake_verify_site

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/verify",
        )
    finally:
        heritage_sites.verify_site = original_verify_site
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "site-1"
    assert response.json()["data"]["is_verified"] is True
    assert response.json()["message"] == "Heritage site verified successfully"

def test_normal_user_cannot_activate_heritage_site():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/activate",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_activate_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_activate_site(db, site_id):
        return SimpleNamespace(
            id=site_id,
            name="Test Heritage Site",
            slug="test-heritage-site",
            short_description=None,
            description=None,
            category="Monument",
            country="India",
            state=None,
            city=None,
            latitude=None,
            longitude=None,
            established_year=None,
            architectural_style=None,
            historical_period=None,
            significance=None,
            preservation_status=None,
            is_verified=True,
            is_active=True,
        )

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_activate_site = heritage_sites.activate_site
    heritage_sites.activate_site = fake_activate_site

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/activate",
        )
    finally:
        heritage_sites.activate_site = original_activate_site
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "site-1"
    assert response.json()["data"]["is_active"] is True
    assert response.json()["message"] == "Heritage site activated successfully"


def test_normal_user_cannot_deactivate_heritage_site():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/deactivate",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_deactivate_heritage_site():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_deactivate_site(db, site_id):
        return SimpleNamespace(
            id=site_id,
            name="Test Heritage Site",
            slug="test-heritage-site",
            short_description=None,
            description=None,
            category="Monument",
            country="India",
            state=None,
            city=None,
            latitude=None,
            longitude=None,
            established_year=None,
            architectural_style=None,
            historical_period=None,
            significance=None,
            preservation_status=None,
            is_verified=True,
            is_active=False,
        )

    from app.api.v1 import heritage_sites

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_deactivate_site = heritage_sites.deactivate_site
    heritage_sites.deactivate_site = fake_deactivate_site

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/deactivate",
        )
    finally:
        heritage_sites.deactivate_site = original_deactivate_site
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "site-1"
    assert response.json()["data"]["is_active"] is False
    assert response.json()["message"] == "Heritage site deactivated successfully"
