from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole


client = TestClient(app)


def test_heritage_site_historical_events_list_is_public():
    class FakeDB:
        pass

    def fake_list_events(db, site_id):
        return []

    from app.api.v1 import heritage_site_historical_event

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_list_events = heritage_site_historical_event.list_events
    heritage_site_historical_event.list_events = fake_list_events

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/historical-events",
        )
    finally:
        heritage_site_historical_event.list_events = original_list_events
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["events"] == []
    assert response.json()["data"]["total"] == 0


def test_heritage_site_historical_event_get_is_public():
    class FakeDB:
        pass

    event = SimpleNamespace(
        id="event-1",
        site_id="site-1",
        title="Foundation",
        description="Historical foundation event",
        event_date="1850-01-01",
        date_precision="YEAR",
        significance="Important historical event",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    def fake_get_event_or_404(db, event_id):
        return event

    from app.api.v1 import heritage_site_historical_event

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_event = heritage_site_historical_event.get_event_or_404
    heritage_site_historical_event.get_event_or_404 = fake_get_event_or_404

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/historical-events/event-1",
        )
    finally:
        heritage_site_historical_event.get_event_or_404 = original_get_event
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "event-1"
    assert response.json()["data"]["site_id"] == "site-1"


def test_normal_user_cannot_create_heritage_site_historical_event():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/historical-events",
            json={
                "title": "Foundation",
                "description": "Historical foundation event",
                "event_date": "1850-01-01",
                "date_precision": "YEAR",
                "significance": "Important historical event",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_heritage_site_historical_event():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_create_event(db, site_id, data):
        return SimpleNamespace(
            id="event-1",
            site_id=site_id,
            title=data.title,
            description=data.description,
            event_date=data.event_date,
            date_precision=data.date_precision,
            significance=data.significance,
            display_order=0,
            is_verified=False,
            is_active=True,
        )

    from app.api.v1 import heritage_site_historical_event

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create_event = heritage_site_historical_event.create_event
    heritage_site_historical_event.create_event = fake_create_event

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/historical-events",
            json={
                "title": "Foundation",
                "description": "Historical foundation event",
                "event_date": "1850-01-01",
                "date_precision": "YEAR",
                "significance": "Important historical event",
            },
        )
    finally:
        heritage_site_historical_event.create_event = original_create_event
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "event-1"
    assert response.json()["data"]["site_id"] == "site-1"


def test_admin_can_update_heritage_site_historical_event():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    existing_event = SimpleNamespace(
        id="event-1",
        site_id="site-1",
        title="Old Title",
        description="Old description",
        event_date="1850-01-01",
        date_precision="YEAR",
        significance="Old significance",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    updated_event = SimpleNamespace(
        id="event-1",
        site_id="site-1",
        title="Updated Title",
        description="Updated description",
        event_date="1851-01-01",
        date_precision="DAY",
        significance="Updated significance",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    def fake_get_event_or_404(db, event_id):
        return existing_event

    def fake_update_event(db, event_id, data):
        return updated_event

    from app.api.v1 import heritage_site_historical_event

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_event = heritage_site_historical_event.get_event_or_404
    original_update_event = heritage_site_historical_event.update_event

    heritage_site_historical_event.get_event_or_404 = fake_get_event_or_404
    heritage_site_historical_event.update_event = fake_update_event

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1/historical-events/event-1",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "date_precision": "DAY",
            },
        )
    finally:
        heritage_site_historical_event.get_event_or_404 = original_get_event
        heritage_site_historical_event.update_event = original_update_event
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "event-1"
    assert response.json()["data"]["title"] == "Updated Title"


def test_admin_can_delete_heritage_site_historical_event():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    event = SimpleNamespace(
        id="event-1",
        site_id="site-1",
        title="Foundation",
        description="Historical foundation event",
        event_date="1850-01-01",
        date_precision="YEAR",
        significance="Important historical event",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    deleted = {"called": False}

    def fake_get_event_or_404(db, event_id):
        return event

    def fake_delete_event(db, event_id):
        deleted["called"] = True

    from app.api.v1 import heritage_site_historical_event

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_event = heritage_site_historical_event.get_event_or_404
    original_delete_event = heritage_site_historical_event.delete_event

    heritage_site_historical_event.get_event_or_404 = fake_get_event_or_404
    heritage_site_historical_event.delete_event = fake_delete_event

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1/historical-events/event-1",
        )
    finally:
        heritage_site_historical_event.get_event_or_404 = original_get_event
        heritage_site_historical_event.delete_event = original_delete_event
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["called"] is True
