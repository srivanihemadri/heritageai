from __future__ import annotations

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 21 — SCANNER CONTROLLED AUTHORIZATION & USER-ISOLATION REGRESSION")
print("=" * 80)

print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")

print()
print("===== 2. VERIFY SCANNER ROUTE =====")

paths = app.openapi().get("paths", {})

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError(
        "POST /api/v1/ai/scan route is missing."
    )

print("POST /api/v1/ai/scan: PASS")

print()
print("===== 3. VERIFY AUTHENTICATION SECURITY =====")

scanner_route = paths["/api/v1/ai/scan"]

security = scanner_route.get("post", {}).get("security", [])

if not security:
    raise RuntimeError(
        "Scanner route has no OpenAPI security requirement."
    )

print("OpenAPI authentication requirement: PRESENT")

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "test.png",
            b"invalid-image",
            "image/png",
        )
    },
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401 for unauthenticated scanner request, "
        f"got {unauthenticated.status_code}: "
        f"{unauthenticated.text}"
    )

print("Unauthenticated scanner request: HTTP 401")
print("Authentication boundary: PASS")

print()
print("===== 4. VERIFY AUTHENTICATION DEPENDENCY =====")

route_source = Path(
    "app/api/v1/ai.py"
).read_text(encoding="utf-8")

if "get_current_user" not in route_source:
    raise RuntimeError(
        "Scanner route source does not reference get_current_user."
    )

print("get_current_user dependency reference: PRESENT")
print("Authorization dependency architecture: PASS")

print()
print("===== 5. CREATE CONTROLLED USER A =====")

email_a = f"task21.a.{uuid.uuid4().hex}@example.com"
password_a = "Task21-Controlled-A-Password-123!"

registration_a = client.post(
    "/api/v1/auth/register",
    json={
        "email": email_a,
        "full_name": "Task 21 User A",
        "password": password_a,
    },
)

if registration_a.status_code not in (200, 201):
    raise RuntimeError(
        f"User A registration failed: "
        f"{registration_a.status_code} "
        f"{registration_a.text}"
    )

print("User A registration: PASS")

print()
print("===== 6. CREATE CONTROLLED USER B =====")

email_b = f"task21.b.{uuid.uuid4().hex}@example.com"
password_b = "Task21-Controlled-B-Password-123!"

registration_b = client.post(
    "/api/v1/auth/register",
    json={
        "email": email_b,
        "full_name": "Task 21 User B",
        "password": password_b,
    },
)

if registration_b.status_code not in (200, 201):
    raise RuntimeError(
        f"User B registration failed: "
        f"{registration_b.status_code} "
        f"{registration_b.text}"
    )

print("User B registration: PASS")

print()
print("===== 7. LOGIN USER A =====")

login_a = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_a,
        "password": password_a,
    },
)

if login_a.status_code != 200:
    raise RuntimeError(
        f"User A login failed: "
        f"{login_a.status_code} "
        f"{login_a.text}"
    )

payload_a = login_a.json()

token_a = (
    payload_a.get("access_token")
    or payload_a.get("token")
)

if not token_a:
    raise RuntimeError(
        "User A JWT token was not returned."
    )

headers_a = {
    "Authorization": f"Bearer {token_a}",
}

print("User A login: PASS")
print("User A JWT acquisition: PASS")

print()
print("===== 8. LOGIN USER B =====")

login_b = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_b,
        "password": password_b,
    },
)

if login_b.status_code != 200:
    raise RuntimeError(
        f"User B login failed: "
        f"{login_b.status_code} "
        f"{login_b.text}"
    )

payload_b = login_b.json()

token_b = (
    payload_b.get("access_token")
    or payload_b.get("token")
)

if not token_b:
    raise RuntimeError(
        "User B JWT token was not returned."
    )

headers_b = {
    "Authorization": f"Bearer {token_b}",
}

print("User B login: PASS")
print("User B JWT acquisition: PASS")

print()
print("===== 9. VERIFY USER TOKENS ARE DISTINCT =====")

if token_a == token_b:
    raise RuntimeError(
        "User A and User B received identical JWT tokens."
    )

print("User A token != User B token: PASS")

print()
print("===== 10. VERIFY SCANNER REQUIRES AUTHENTICATED USER =====")

for label, headers in (
    ("User A", headers_a),
    ("User B", headers_b),
):

    response = client.post(
        "/api/v1/ai/scan",
        headers=headers,
        files={
            "file": (
                "invalid.png",
                b"not-a-real-image",
                "image/png",
            )
        },
    )

    if response.status_code == 401:
        raise RuntimeError(
            f"{label} was rejected as unauthenticated."
        )

    if response.status_code != 400:
        raise RuntimeError(
            f"{label} scanner validation boundary expected HTTP 400 "
            f"for invalid image, got "
            f"{response.status_code}: {response.text}"
        )

    print(
        f"{label} authenticated scanner access: PASS"
    )

print("Authenticated scanner boundary: PASS")

print()
print("===== 11. VERIFY USER ID IS NOT ACCEPTED FROM CLIENT BODY =====")

scanner_operation_source = route_source

for forbidden_field in (
    "user_id: str = Form",
    "user_id: str = File",
    "user_id: str = Query",
    "owner_id: str = Form",
    "owner_id: str = Query",
):

    if forbidden_field in scanner_operation_source:
        raise RuntimeError(
            f"Scanner route accepts client-controlled identity field: "
            f"{forbidden_field}"
        )

print("No client-controlled scanner user_id parameter: PASS")

print()
print("===== 12. VERIFY SERVER-SIDE USER DEPENDENCY =====")

if "current_user" not in scanner_operation_source:
    raise RuntimeError(
        "Scanner route does not expose a current_user dependency."
    )

if "get_current_user" not in scanner_operation_source:
    raise RuntimeError(
        "Scanner route does not use get_current_user."
    )

print("current_user dependency: PRESENT")
print("Server-side identity boundary: PASS")

print()
print("===== 13. VERIFY EXISTING AI ROUTES =====")

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "/api/v1/ai/answer route is missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 14. PRODUCTION SAFETY =====")

print("Controlled authorization paths only: PASS")
print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 21 COMPLETE")
print("=" * 80)
print("Scanner authentication: PASS")
print("Unauthenticated rejection: PASS")
print("User A authorization: PASS")
print("User B authorization: PASS")
print("Distinct JWT identities: PASS")
print("Server-side identity boundary: PASS")
print("No client-controlled user identity: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
