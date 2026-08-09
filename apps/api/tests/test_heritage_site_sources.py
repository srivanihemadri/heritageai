from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.heritage_site_source import SourceType
from app.models.user import UserRole

client = TestClient(app)


def make_source(
    source_id="source-1",
    site_id="site-1",
    is_verified=False,
    is_active=True,
):
    return SimpleNamespace(
        id=source_id,
        site_id=site_id,
        source_type=SourceType.GOVERNMENT,
        title="Archaeological Survey of India",
        author=None,
        organization="Archaeological Survey of India",
        publisher=None,
        publication_date=None,
        url="https://example.com/source",
        citation_text="Official heritage documentation",
        language="en",
        display_order=0,
        is_verified=is_verified,
        is_active=is_active,
    )


def test_sources_list_is_public():
    class FakeDB:
        pass

    def fake_list_sources(db, site_id):
        return [make_source()]

    from app.api.v1 import heritage_site_source

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_list_sources = heritage_site_source.list_sources
    heritage_site_source.list_sources = fake_list_sources

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/sources",
        )
    finally:
        heritage_site_source.list_sources = original_list_sources
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["total"] == 1
    assert response.json()["data"]["sources"][0]["id"] == "source-1"


def test_normal_user_cannot_create_source():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/sources",
            json={
                "source_type": "GOVERNMENT",
                "title": "Archaeological Survey of India",
                "organization": "Archaeological Survey of India",
                "language": "en",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_source():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    created_source = make_source()

    def fake_create_source(db, source):
        return created_source

    from app.api.v1 import heritage_site_source

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create_source = heritage_site_source.create_source
    heritage_site_source.create_source = fake_create_source

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/sources",
            json={
                "source_type": "GOVERNMENT",
                "title": "Archaeological Survey of India",
                "organization": "Archaeological Survey of India",
                "language": "en",
            },
        )
    finally:
        heritage_site_source.create_source = original_create_source
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "source-1"
    assert response.json()["data"]["site_id"] == "site-1"


def test_admin_can_update_source():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    source = make_source()

    def fake_get_source_or_404(db, source_id):
        return source

    def fake_update_source(db, source):
        return source

    from app.api.v1 import heritage_site_source

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get = heritage_site_source.get_source_or_404
    original_update = heritage_site_source.update_source

    heritage_site_source.get_source_or_404 = fake_get_source_or_404
    heritage_site_source.update_source = fake_update_source

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1/sources/source-1",
            json={
                "title": "Updated Heritage Source",
            },
        )
    finally:
        heritage_site_source.get_source_or_404 = original_get
        heritage_site_source.update_source = original_update
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_admin_can_delete_source():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    source = make_source()
    deleted = {"value": False}

    def fake_get_source_or_404(db, source_id):
        return source

    def fake_delete_source(db, source_id):
        deleted["value"] = True

    from app.api.v1 import heritage_site_source

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get = heritage_site_source.get_source_or_404
    original_delete = heritage_site_source.delete_source

    heritage_site_source.get_source_or_404 = fake_get_source_or_404
    heritage_site_source.delete_source = fake_delete_source

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1/sources/source-1",
        )
    finally:
        heritage_site_source.get_source_or_404 = original_get
        heritage_site_source.delete_source = original_delete
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["value"] is True


def test_source_from_different_site_is_not_accessible():
    class FakeDB:
        pass

    source = make_source(
        source_id="source-1",
        site_id="different-site",
    )

    def fake_get_source_or_404(db, source_id):
        return source

    from app.api.v1 import heritage_site_source

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get = heritage_site_source.get_source_or_404
    heritage_site_source.get_source_or_404 = fake_get_source_or_404

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/sources/source-1",
        )
    finally:
        heritage_site_source.get_source_or_404 = original_get
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "HERITAGE_SITE_SOURCE_NOT_FOUND"
