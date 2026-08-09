from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole

client = TestClient(app)


def test_media_list_is_public():
    class FakeDB:
        pass

    def fake_list_site_media(db, site_id):
        return []

    from app.api.v1 import heritage_site_media

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_list = heritage_site_media.list_site_media
    heritage_site_media.list_site_media = fake_list_site_media

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/media",
        )
    finally:
        heritage_site_media.list_site_media = original_list
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["media"] == []
    assert response.json()["data"]["total"] == 0


def test_normal_user_cannot_create_media():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/media",
            json={
                "media_type": "IMAGE",
                "storage_key": "heritage/site-1/image.jpg",
                "url": "https://example.com/image.jpg",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_media():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_create_site_media(db, site_id, data):
        return SimpleNamespace(
            id="media-1",
            site_id=site_id,
            media_type=data.media_type,
            storage_key=data.storage_key,
            url=data.url,
            title=data.title,
            alt_text=data.alt_text,
            display_order=data.display_order,
            is_primary=data.is_primary,
            is_active=True,
        )

    from app.api.v1 import heritage_site_media

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create = heritage_site_media.create_site_media
    heritage_site_media.create_site_media = fake_create_site_media

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/media",
            json={
                "media_type": "IMAGE",
                "storage_key": "heritage/site-1/image.jpg",
                "url": "https://example.com/image.jpg",
            },
        )
    finally:
        heritage_site_media.create_site_media = original_create
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "media-1"
    assert response.json()["data"]["site_id"] == "site-1"


def test_admin_can_update_media():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_update_site_media(db, site_id, media_id, data):
        return SimpleNamespace(
            id=media_id,
            site_id="site-1",
            media_type="IMAGE",
            storage_key="heritage/site-1/updated.jpg",
            url="https://example.com/updated.jpg",
            title=data.title,
            alt_text=None,
            display_order=0,
            is_primary=False,
            is_active=True,
        )

    from app.api.v1 import heritage_site_media

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_update = heritage_site_media.update_site_media
    heritage_site_media.update_site_media = fake_update_site_media

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1/media/media-1",
            json={
                "title": "Updated Image",
            },
        )
    finally:
        heritage_site_media.update_site_media = original_update
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "media-1"
    assert response.json()["data"]["title"] == "Updated Image"


def test_admin_can_delete_media():
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

    def fake_delete_site_media(db, site_id, media_id):
        deleted["value"] = True

    from app.api.v1 import heritage_site_media

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_delete = heritage_site_media.delete_site_media
    heritage_site_media.delete_site_media = fake_delete_site_media

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1/media/media-1",
        )
    finally:
        heritage_site_media.delete_site_media = original_delete
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["value"] is True
