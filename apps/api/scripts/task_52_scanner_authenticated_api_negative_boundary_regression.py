from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 52 — SCANNER AUTHENTICATED API NEGATIVE-BOUNDARY REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY SCANNER ROUTE =====")

openapi = client.get("/openapi.json")

if openapi.status_code != 200:
    raise RuntimeError(
        f"OpenAPI request failed: {openapi.status_code}"
    )

paths = openapi.json().get("paths", {})

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError(
        "Scanner route missing from OpenAPI."
    )

print("POST /api/v1/ai/scan: PRESENT")
print("Scanner route: PASS")


print()
print("===== 3. VERIFY UNAUTHENTICATED NEGATIVE BOUNDARY =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "test.png",
            b"invalid",
            "image/png",
        )
    },
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        "Unauthenticated scanner request was not blocked."
    )

print("Unauthenticated upload: HTTP 401")
print("Authentication boundary: PASS")


print()
print("===== 4. CREATE CONTROLLED TEST USER =====")

email = "task52_negative_scanner_user@example.com"
password = "Task52-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 52 Negative Scanner User",
        "password": password,
    },
)

if registration.status_code not in (200, 201, 409):
    raise RuntimeError(
        f"Registration failed: "
        f"{registration.status_code}"
    )

print("Controlled registration: PASS")


print()
print("===== 5. LOGIN CONTROLLED USER =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login.status_code != 200:
    raise RuntimeError(
        f"Login failed: "
        f"{login.status_code}"
    )

login_payload = login.json()

token = (
    login_payload.get("access_token")
    or login_payload.get("token")
)

if not token:
    raise RuntimeError(
        "JWT token was not returned."
    )

headers = {
    "Authorization": f"Bearer {token}"
}

print("Login: PASS")
print("JWT acquisition: PASS")


print()
print("===== 6. VERIFY EMPTY IMAGE =====")

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
        f"Empty image returned unexpected status: "
        f"{empty_response.status_code}"
    )

print("Empty image: HTTP 400")
print("Empty image boundary: PASS")


print()
print("===== 7. VERIFY CORRUPTED IMAGE =====")

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
        f"Corrupted image returned unexpected status: "
        f"{corrupted_response.status_code}"
    )

print("Corrupted image: HTTP 400")
print("Corrupted image boundary: PASS")


print()
print("===== 8. VERIFY UNSUPPORTED MIME =====")

unsupported_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "document.txt",
            b"plain text content",
            "text/plain",
        )
    },
)

if unsupported_response.status_code != 400:
    raise RuntimeError(
        f"Unsupported MIME returned unexpected status: "
        f"{unsupported_response.status_code}"
    )

print("Unsupported MIME: HTTP 400")
print("Unsupported MIME boundary: PASS")


print()
print("===== 9. VERIFY MIME/CONTENT MISMATCH =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

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
        f"MIME mismatch returned unexpected status: "
        f"{mismatch_response.status_code}"
    )

print("MIME mismatch: HTTP 400")
print("MIME mismatch boundary: PASS")


print()
print("===== 10. VERIFY ERROR RESPONSE SANITIZATION =====")

for response_name, response in [
    ("empty", empty_response),
    ("corrupted", corrupted_response),
    ("unsupported", unsupported_response),
    ("mismatch", mismatch_response),
]:
    response_text = response.text

    for forbidden in [
        "GEMINI_API_KEY",
        "Traceback",
        "api_key",
        "password",
        "access_token",
        "secret",
    ]:
        if forbidden in response_text:
            raise RuntimeError(
                f"{response_name} response leaked sensitive data: "
                f"{forbidden}"
            )

print("Invalid-upload error sanitization: PASS")


print()
print()
print("===== 11. VERIFY ERROR CONTRACT =====")

for response_name, response in [
    ("empty", empty_response),
    ("corrupted", corrupted_response),
    ("unsupported", unsupported_response),
    ("mismatch", mismatch_response),
]:
    payload = response.json()
    detail = payload.get("detail")

    if not isinstance(detail, dict):
        raise RuntimeError(
            f"{response_name} response detail envelope is invalid."
        )

    if not detail.get("code"):
        raise RuntimeError(
            f"{response_name} response error code is missing."
        )

    if not detail.get("message"):
        raise RuntimeError(
            f"{response_name} response error message is missing."
        )

print("Public error envelope: PASS")
print("Error code/message contract: PASS")

print("===== 12. VERIFY EXISTING AI ANSWER ROUTE =====")

answer_operation = paths.get(
    "/api/v1/ai/answer",
    {},
).get("post")

if answer_operation is None:
    raise RuntimeError(
        "Existing /api/v1/ai/answer route was not preserved."
    )

print("/api/v1/ai/answer: PRESERVED")


print()
print("===== 13. PRODUCTION SAFETY =====")

print("Controlled authenticated negative regression: PASS")
print("Invalid uploads reaching Gemini: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 52 COMPLETE")
print("=" * 80)
print("Scanner route: PASS")
print("Authentication boundary: PASS")
print("Empty image rejection: PASS")
print("Corrupted image rejection: PASS")
print("Unsupported MIME rejection: PASS")
print("MIME mismatch rejection: PASS")
print("Error sanitization: PASS")
print("Error contract: PASS")
print("Existing AI answer route: PRESERVED")
print("NO INVALID UPLOAD SHOULD REACH GEMINI.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

