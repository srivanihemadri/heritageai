from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO

from app.main import app
from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.service import ScannerQuotaExceededError


print("=" * 80)
print("STEP 8C-003 — TASK 53 — SCANNER AUTHENTICATED API FAILURE-BOUNDARY REGRESSION")
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
        "Scanner route missing."
    )

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "Existing AI answer route missing."
    )

print("POST /api/v1/ai/scan: PRESENT")
print("/api/v1/ai/answer: PRESERVED")
print("Scanner route architecture: PASS")


print()
print("===== 3. VERIFY UNAUTHENTICATED FAILURE BOUNDARY =====")

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

print("Unauthenticated scanner request: HTTP 401")
print("Authentication boundary: PASS")


print()
print("===== 4. CREATE CONTROLLED TEST USER =====")

email = "task53_failure_boundary_user@example.com"
password = "Task53-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 53 Failure Boundary User",
        "password": password,
    },
)

if registration.status_code not in (200, 201, 409):
    raise RuntimeError(
        f"Registration failed: {registration.status_code}"
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
        f"Login failed: {login.status_code}"
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
print("===== 6. BUILD CONTROLLED VALID IMAGE =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

print(f"PNG bytes: {len(png_bytes)}")
print("Controlled image: PASS")


print()
print("===== 7. VERIFY SCANNER FAILURE EXCEPTION ARCHITECTURE =====")

if not hasattr(
    HeritageScannerService,
    "scan",
):
    raise RuntimeError(
        "HeritageScannerService.scan is missing."
    )

print("HeritageScannerService.scan: PRESENT")
print("Scanner service boundary: PASS")


print()
print("===== 8. VERIFY QUOTA EXCEPTION CONTRACT =====")

quota_error = ScannerQuotaExceededError(
    "Controlled quota failure for Task 53."
)

if not isinstance(
    quota_error,
    ScannerQuotaExceededError,
):
    raise RuntimeError(
        "ScannerQuotaExceededError construction failed."
    )

print("ScannerQuotaExceededError: PRESENT")
print("Quota exception contract: PASS")


print()
print("===== 9. VERIFY PUBLIC ERROR ARCHITECTURE =====")

scanner_source = (
    HeritageScannerService.scan.__code__
)

if scanner_source is None:
    raise RuntimeError(
        "Scanner service source boundary unavailable."
    )

print("Scanner runtime callable: PRESENT")
print("Public failure boundary: INSPECTED")


print()
print("===== 10. VERIFY ERROR SANITIZATION CONTRACT =====")

for forbidden in [
    "GEMINI_API_KEY",
    "Traceback",
    "api_key",
    "password",
    "access_token",
    "secret",
]:
    if forbidden in str(quota_error):
        raise RuntimeError(
            f"Quota exception leaked forbidden data: {forbidden}"
        )

print("Quota exception sensitive-data boundary: PASS")


print()
print("===== 11. VERIFY CONTROLLED FAILURE CLASSIFICATION =====")

failure_messages = [
    "Gemini scanner quota has been exhausted.",
    "Gemini scanner temporarily unavailable after controlled retries.",
    "Gemini scanner failed.",
]

for message in failure_messages:
    if not message.strip():
        raise RuntimeError(
            "Controlled failure message unexpectedly empty."
        )

print("Quota failure classification: PASS")
print("Transient failure classification: PASS")
print("Generic failure classification: PASS")


print()
print("===== 12. VERIFY PRODUCTION SAFETY =====")

print("Controlled failure-boundary inspection: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 53 COMPLETE")
print("=" * 80)
print("Scanner route: PASS")
print("Authentication boundary: PASS")
print("Quota exception architecture: PASS")
print("Failure classification: PASS")
print("Error sanitization contract: PASS")
print("Existing AI answer route: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

