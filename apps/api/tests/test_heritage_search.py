from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


client = TestClient(app)


def test_heritage_sites_search_filters_and_pagination():
    captured = {}

    class FakeQuery:
        def filter(self, *args):
            return self

        def with_entities(self, *args):
            return self

        def scalar(self):
            return 7

        def order_by(self, *args):
            return self

        def offset(self, value):
            captured["offset"] = value
            return self

        def limit(self, value):
            captured["limit"] = value
            return self

        def all(self):
            return []

    class FakeDB:
        def query(self, *args):
            return FakeQuery()

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        response = client.get(
            "/api/v1/heritage-sites",
            params={
                "search": "temple",
                "category": "Monument",
                "country": "India",
                "state": "Andhra Pradesh",
                "city": "Vijayawada",
                "page": 2,
                "page_size": 5,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["total"] == 7
    assert body["data"]["page"] == 2
    assert body["data"]["page_size"] == 5
    assert body["data"]["total_pages"] == 2

    assert captured["offset"] == 5
    assert captured["limit"] == 5


def test_heritage_sites_page_size_has_maximum():
    response = client.get(
        "/api/v1/heritage-sites",
        params={
            "page_size": 101,
        },
    )

    assert response.status_code == 422


def test_heritage_sites_page_must_be_positive():
    response = client.get(
        "/api/v1/heritage-sites",
        params={
            "page": 0,
        },
    )

    assert response.status_code == 422
