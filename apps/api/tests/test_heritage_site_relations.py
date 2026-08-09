from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole


client = TestClient(app)


def test_heritage_site_relations_list_is_public():
    class FakeDB:
        pass

    def fake_list_relations(db, site_id):
        return []

    from app.api.v1 import heritage_site_relation

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_list_relations = heritage_site_relation.list_relations
    heritage_site_relation.list_relations = fake_list_relations

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/relations",
        )
    finally:
        heritage_site_relation.list_relations = original_list_relations
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["relations"] == []
    assert response.json()["data"]["total"] == 0


def test_heritage_site_relation_get_is_public():
    class FakeDB:
        pass

    relation = SimpleNamespace(
        id="relation-1",
        source_site_id="site-1",
        target_site_id="22222222-2222-2222-2222-222222222222",
        relation_type="RELATED_TO",
        description="Related heritage site",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    def fake_get_relation_or_404(db, relation_id):
        return relation

    from app.api.v1 import heritage_site_relation

    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_relation = heritage_site_relation.get_relation_or_404
    heritage_site_relation.get_relation_or_404 = fake_get_relation_or_404

    try:
        response = client.get(
            "/api/v1/heritage-sites/site-1/relations/relation-1",
        )
    finally:
        heritage_site_relation.get_relation_or_404 = original_get_relation
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "relation-1"
    assert response.json()["data"]["source_site_id"] == "site-1"


def test_normal_user_cannot_create_heritage_site_relation():
    def deny_admin():
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    app.dependency_overrides[get_current_admin] = deny_admin

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/relations",
            json={
                "target_site_id": "22222222-2222-2222-2222-222222222222",
                "relation_type": "RELATED_TO",
                "description": "Related heritage site",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_create_heritage_site_relation():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    def fake_create_relation(db, site_id, data):
        return SimpleNamespace(
            id="relation-1",
            source_site_id=site_id,
            target_site_id=data.target_site_id,
            relation_type=data.relation_type,
            description=data.description,
            display_order=0,
            is_verified=False,
            is_active=True,
        )

    from app.api.v1 import heritage_site_relation

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_create_relation = heritage_site_relation.create_relation
    heritage_site_relation.create_relation = fake_create_relation

    try:
        response = client.post(
            "/api/v1/heritage-sites/site-1/relations",
            json={
                "target_site_id": "22222222-2222-2222-2222-222222222222",
                "relation_type": "RELATED_TO",
                "description": "Related heritage site",
            },
        )
    finally:
        heritage_site_relation.create_relation = original_create_relation
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "relation-1"
    assert response.json()["data"]["source_site_id"] == "site-1"


def test_admin_can_update_heritage_site_relation():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    existing_relation = SimpleNamespace(
        id="relation-1",
        source_site_id="site-1",
        target_site_id="22222222-2222-2222-2222-222222222222",
        relation_type="RELATED_TO",
        description="Old description",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    updated_relation = SimpleNamespace(
        id="relation-1",
        source_site_id="site-1",
        target_site_id="22222222-2222-2222-2222-222222222222",
        relation_type="PART_OF",
        description="Updated description",
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    def fake_get_relation_or_404(db, relation_id):
        return existing_relation

    def fake_update_relation(db, relation_id, data):
        return updated_relation

    from app.api.v1 import heritage_site_relation

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_relation = heritage_site_relation.get_relation_or_404
    original_update_relation = heritage_site_relation.update_relation

    heritage_site_relation.get_relation_or_404 = fake_get_relation_or_404
    heritage_site_relation.update_relation = fake_update_relation

    try:
        response = client.patch(
            "/api/v1/heritage-sites/site-1/relations/relation-1",
            json={
                "relation_type": "PART_OF",
                "description": "Updated description",
            },
        )
    finally:
        heritage_site_relation.get_relation_or_404 = original_get_relation
        heritage_site_relation.update_relation = original_update_relation
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "relation-1"
    assert response.json()["data"]["relation_type"] == "PART_OF"


def test_admin_can_delete_heritage_site_relation():
    admin = SimpleNamespace(
        id="admin-1",
        full_name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True,
    )

    class FakeDB:
        pass

    relation = SimpleNamespace(
        id="relation-1",
        source_site_id="site-1",
        target_site_id="22222222-2222-2222-2222-222222222222",
        relation_type="RELATED_TO",
        description=None,
        display_order=0,
        is_verified=False,
        is_active=True,
    )

    deleted = {"value": False}

    def fake_get_relation_or_404(db, relation_id):
        return relation

    def fake_delete_relation(db, relation_id):
        deleted["value"] = True

    from app.api.v1 import heritage_site_relation

    app.dependency_overrides[get_current_admin] = lambda: admin
    app.dependency_overrides[get_db] = lambda: FakeDB()

    original_get_relation = heritage_site_relation.get_relation_or_404
    original_delete_relation = heritage_site_relation.delete_relation

    heritage_site_relation.get_relation_or_404 = fake_get_relation_or_404
    heritage_site_relation.delete_relation = fake_delete_relation

    try:
        response = client.delete(
            "/api/v1/heritage-sites/site-1/relations/relation-1",
        )
    finally:
        heritage_site_relation.get_relation_or_404 = original_get_relation
        heritage_site_relation.delete_relation = original_delete_relation
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert deleted["value"] is True
