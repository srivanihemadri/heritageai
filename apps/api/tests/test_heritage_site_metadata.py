from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole

client = TestClient(app)


def test_metadata_list_is_public():
    class FakeDB:
        pass

    def fake_list_site_metadata(db, site_id):
        return []

    from app.api.v1 import heritage_site_metadata

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_list = heritage_site_metadata.list_site_metadata
    heritage_site_metadata.list_site_metadata = fake_list_site_metadata

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/metadata",
        )
    finally:
        heritage_site_metadata.list_site_metadata = original_list
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["metadata"] == []
    assert response.json()["data"]["total"] == 0


def test_normal_user_cannot_create_metadata():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/metadata",
            json={
                "metadata_type": "history",
                "title": "History",
                "content": "Historical information.",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_metadata():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_create_site_metadata(db, site_id, data):
        return SimpleNamespace(
            id="metadata-1",
            site_id=site_id,
            metadata_type=data.metadata_type,
            title=data.title,
            content=data.content,
            source=data.source,
            source_url=data.source_url,
            language=data.language,
            display_order=data.display_order,
            is_verified=False,
            is_active=True,
        )

    from app.api.v1 import heritage_site_metadata

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create = heritage_site_metadata.create_site_metadata
    heritage_site_metadata.create_site_metadata = fake_create_site_metadata

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/metadata",
            json={
                "metadata_type": "history",
                "title": "History",
                "content": "Historical information.",
            },
        )
    finally:
        heritage_site_metadata.create_site_metadata = original_create
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "metadata-1"
    assert response.json()["data"]["site_id"] == "site-1"


def test_admin_can_update_metadata():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    metadata = SimpleNamespace(
        id="metadata-1",
        site_id="site-1",
        metadata_type="history",
        title="Updated History",
        content="Updated historical information.",
        source=None,
        source_url=None,
        language="en",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    def fake_get_site_metadata(db, metadata_id):
        return metadata

    def fake_update_site_metadata(db, metadata_id, data):
        metadata.title = data.title or metadata.title
        return metadata

    from app.api.v1 import heritage_site_metadata

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get = heritage_site_metadata.get_site_metadata
    original_update = heritage_site_metadata.update_site_metadata

    heritage_site_metadata.get_site_metadata = fake_get_site_metadata
    heritage_site_metadata.update_site_metadata = fake_update_site_metadata

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1/metadata/metadata-1",
            json={
                "title": "Updated History",
            },
        )
    finally:
        heritage_site_metadata.get_site_metadata = original_get
        heritage_site_metadata.update_site_metadata = original_update
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Updated History"


def test_admin_can_delete_metadata():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    metadata = SimpleNamespace(
        id="metadata-1",
        site_id="site-1",
    )

    deleted = {"value": False}

    def fake_get_site_metadata(db, metadata_id):
        return metadata

    def fake_delete_site_metadata(db, metadata_id):
        deleted["value"] = True

    from app.api.v1 import heritage_site_metadata

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get = heritage_site_metadata.get_site_metadata
    original_delete = heritage_site_metadata.delete_site_metadata

    heritage_site_metadata.get_site_metadata = fake_get_site_metadata
    heritage_site_metadata.delete_site_metadata = fake_delete_site_metadata

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1/metadata/metadata-1",
        )
    finally:
        heritage_site_metadata.get_site_metadata = original_get
        heritage_site_metadata.delete_site_metadata = original_delete
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["value"] is True
