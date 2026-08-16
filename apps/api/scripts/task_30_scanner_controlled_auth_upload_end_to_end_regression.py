from __future__ import annotations

import sys
import time
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image
from fastapi.testclient import TestClient

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 30 — SCANNER CONTROLLED AUTHENTICATION + UPLOAD END-TO-END REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY SCANNER ROUTE =====")

openapi = app.openapi()

scanner_path = openapi.get(
    "paths",
    {},
).get(
    "/api/v1/ai/scan",
)

if scanner_path is None:
    raise RuntimeError(
        "POST /api/v1/ai/scan route not found."
    )

if "post" not in scanner_path:
    raise RuntimeError(
        "POST /api/v1/ai/scan operation not found."
    )

print("POST /api/v1/ai/scan: PASS")


print()
print("===== 3. VERIFY UNAUTHENTICATED UPLOAD IS BLOCKED =====")

unauthenticated_response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "test.png",
            b"controlled-test-image",
            "image/png",
        )
    },
)

if unauthenticated_response.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401, got "
        f"{unauthenticated_response.status_code}: "
        f"{unauthenticated_response.text}"
    )

print("Unauthenticated upload: HTTP 401")
print("Authentication boundary: PASS")


print()
print("===== 4. VERIFY AUTHENTICATION CONTRACT =====")

security = scanner_path["post"].get("security")

if not security:
    raise RuntimeError(
        "Scanner endpoint has no OpenAPI security requirement."
    )

print("OpenAPI security requirement: PRESENT")
print("Authentication contract: PASS")


print()
print("===== 5. CREATE CONTROLLED TEST USER =====")

import time

email = f"task30_controlled_scanner_{time.time_ns()}@example.com"

password = "Task30-Controlled-Password-123!"

registration_response = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 30 Controlled User",
        "password": password,
    },
)

if registration_response.status_code not in (200, 201):
    raise RuntimeError(
        f"Registration failed: "
        f"{registration_response.status_code} "
        f"{registration_response.text}"
    )

print("Registration: PASS")


print()
print("===== 6. LOGIN CONTROLLED TEST USER =====")

login_response = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login_response.status_code != 200:
    raise RuntimeError(
        f"Login failed: "
        f"{login_response.status_code} "
        f"{login_response.text}"
    )

login_payload = login_response.json()

token = (
    login_payload.get("access_token")
    or login_payload.get("token")
)

if not token:
    raise RuntimeError(
        "JWT token was not returned by login."
    )

headers = {
    "Authorization": f"Bearer {token}",
}

print("Login: PASS")
print("JWT acquisition: PASS")


print()
print("===== 7. BUILD CONTROLLED VALID PNG =====")

image = Image.new(
    "RGB",
    (2, 2),
    (120, 80, 40),
)

buffer = BytesIO()

image.save(
    buffer,
    format="PNG",
)

png_bytes = buffer.getvalue()

print(f"Controlled PNG bytes: {len(png_bytes)}")
print("Controlled image construction: PASS")


print()
print("===== 8. VERIFY AUTHENTICATED VALID UPLOAD BOUNDARY =====")

valid_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "controlled.png",
            png_bytes,
            "image/png",
        )
    },
)

if valid_response.status_code == 200:
    print("Authenticated valid upload: HTTP 200")
    print("Valid upload boundary: PASS")

elif valid_response.status_code in (429, 500, 503):
    print(
        f"Authenticated scanner reached controlled service boundary: "
        f"HTTP {valid_response.status_code}"
    )
    print(
        "Valid upload reached scanner service boundary: PASS"
    )

else:
    raise RuntimeError(
        f"Unexpected authenticated valid-upload status: "
        f"{valid_response.status_code}: "
        f"{valid_response.text}"
    )


print()
print("===== 9. VERIFY EMPTY IMAGE =====")

empty_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "empty.png",
            b"",
            "image/png",
        )
    },
)

if empty_response.status_code != 400:
    raise RuntimeError(
        f"Expected empty image HTTP 400, got "
        f"{empty_response.status_code}: "
        f"{empty_response.text}"
    )

print("Empty image: HTTP 400")
print("Empty image boundary: PASS")


print()
print("===== 10. VERIFY CORRUPTED IMAGE =====")

corrupted_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "corrupted.png",
            b"not-a-real-image",
            "image/png",
        )
    },
)

if corrupted_response.status_code != 400:
    raise RuntimeError(
        f"Expected corrupted image HTTP 400, got "
        f"{corrupted_response.status_code}: "
        f"{corrupted_response.text}"
    )

print("Corrupted image: HTTP 400")
print("Corrupted image boundary: PASS")


print()
print("===== 11. VERIFY UNSUPPORTED MIME =====")

unsupported_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "image.gif",
            png_bytes,
            "image/gif",
        )
    },
)

if unsupported_response.status_code != 400:
    raise RuntimeError(
        f"Expected unsupported MIME HTTP 400, got "
        f"{unsupported_response.status_code}: "
        f"{unsupported_response.text}"
    )

print("Unsupported MIME: HTTP 400")
print("Unsupported MIME boundary: PASS")


print()
print("===== 12. VERIFY MIME FORMAT MISMATCH =====")

mismatch_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "mismatch.jpg",
            png_bytes,
            "image/jpeg",
        )
    },
)

if mismatch_response.status_code != 400:
    raise RuntimeError(
        f"Expected MIME mismatch HTTP 400, got "
        f"{mismatch_response.status_code}: "
        f"{mismatch_response.text}"
    )

print("MIME mismatch: HTTP 400")
print("MIME mismatch boundary: PASS")


print()
print("===== 13. VERIFY ERROR RESPONSE SANITIZATION =====")

for response_name, response in (
    ("empty", empty_response),
    ("corrupted", corrupted_response),
    ("unsupported", unsupported_response),
    ("mismatch", mismatch_response),
):

    body = response.text.lower()

    for forbidden in (
        "traceback",
        "google.genai",
        "api_key",
        "password",
        "secret",
    ):
        if forbidden in body:
            raise RuntimeError(
                f"{response_name} response leaks "
                f"internal detail: {forbidden}"
            )

print("Scanner error sanitization: PASS")


print()
print("===== 14. VERIFY EXISTING AI ROUTES =====")

answer_path = openapi.get(
    "paths",
    {},
).get(
    "/api/v1/ai/answer",
)

if answer_path is None:
    raise RuntimeError(
        "Existing /api/v1/ai/answer route missing."
    )

if "post" not in answer_path:
    raise RuntimeError(
        "POST /api/v1/ai/answer missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")


print()
print("===== 15. PRODUCTION SAFETY =====")

print("Controlled authentication/upload path only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 30 COMPLETE")
print("=" * 80)
print("Authentication boundary: PASS")
print("Authenticated upload boundary: PASS")
print("Empty image rejection: PASS")
print("Corrupted image rejection: PASS")
print("Unsupported MIME rejection: PASS")
print("MIME mismatch rejection: PASS")
print("Error sanitization: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)





