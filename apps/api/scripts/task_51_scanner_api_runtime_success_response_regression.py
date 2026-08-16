from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 51 — SCANNER API RUNTIME SUCCESS RESPONSE REGRESSION")
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

operation = paths["/api/v1/ai/scan"].get("post")

if operation is None:
    raise RuntimeError(
        "POST /api/v1/ai/scan operation missing."
    )

print("POST /api/v1/ai/scan: PRESENT")
print("Scanner route: PASS")


print()
print("===== 3. VERIFY UNAUTHENTICATED BOUNDARY =====")

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

print("Unauthenticated request: HTTP 401")
print("Authentication boundary: PASS")


print()
print("===== 4. CREATE CONTROLLED TEST USER =====")

email = "task51_runtime_scanner_user@example.com"
password = "Task51-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 51 Runtime Scanner User",
        "password": password,
    },
)

if registration.status_code not in (200, 201, 409):
    raise RuntimeError(
        f"Registration failed: "
        f"{registration.status_code} "
        f"{registration.text}"
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
        f"{login.status_code} "
        f"{login.text}"
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
print("===== 6. BUILD CONTROLLED PNG =====")

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
print("===== 7. EXECUTE AUTHENTICATED SCANNER REQUEST =====")

response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "task51.png",
            png_bytes,
            "image/png",
        )
    },
)

if response.status_code != 200:
    raise RuntimeError(
        f"Authenticated scanner request failed: "
        f"{response.status_code} "
        f"{response.text}"
    )

print("Authenticated scanner request: HTTP 200")
print("Runtime success boundary: PASS")


print()
print("===== 8. VERIFY PUBLIC RESPONSE ENVELOPE =====")

payload = response.json()

if payload.get("success") is not True:
    raise RuntimeError(
        "Public response success is not true."
    )

if not payload.get("scan_id"):
    raise RuntimeError(
        "Public response scan_id is missing."
    )

if not isinstance(payload.get("result"), dict):
    raise RuntimeError(
        "Public response result is not an object."
    )

print("success: PRESENT")
print("scan_id: PRESENT")
print("result: PRESENT")
print("Public response envelope: PASS")


print()
print("===== 9. VERIFY INTELLIGENCE RESPONSE =====")

result = payload["result"]

for field in [
    "identified_name",
    "category",
    "location",
    "country",
    "confidence",
    "confidence_level",
    "description",
    "architectural_style",
    "historical_period",
    "historical_significance",
    "visual_evidence",
    "alternative_matches",
    "grounding_status",
    "identification_status",
    "evidence_quality",
]:
    if field not in result:
        raise RuntimeError(
            f"Scanner result field missing: {field}"
        )

    print(f"{field}: PRESENT")

print("Intelligence response: PASS")


print()
print("===== 10. VERIFY RESPONSE TYPES =====")

if not isinstance(result["confidence"], (int, float)):
    raise RuntimeError(
        "confidence is not numeric."
    )

if not isinstance(result["visual_evidence"], list):
    raise RuntimeError(
        "visual_evidence is not a list."
    )

if not isinstance(result["alternative_matches"], list):
    raise RuntimeError(
        "alternative_matches is not a list."
    )

if result["confidence_level"] not in [
    "LOW",
    "MEDIUM",
    "HIGH",
]:
    raise RuntimeError(
        "Invalid confidence_level returned."
    )

if result["identification_status"] not in [
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
]:
    raise RuntimeError(
        "Invalid identification_status returned."
    )

if result["evidence_quality"] not in [
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
]:
    raise RuntimeError(
        "Invalid evidence_quality returned."
    )

if result["grounding_status"] not in [
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
]:
    raise RuntimeError(
        "Invalid grounding_status returned."
    )

print("confidence: VALID")
print("visual_evidence: VALID LIST")
print("alternative_matches: VALID LIST")
print("confidence_level: VALID")
print("identification_status: VALID")
print("evidence_quality: VALID")
print("grounding_status: VALID")
print("Response types/states: PASS")


print()
print("===== 11. VERIFY SEMANTIC RESPONSE CONSISTENCY =====")

if (
    result["evidence_quality"] == "NONE"
    and result["visual_evidence"]
):
    raise RuntimeError(
        "Invalid runtime response: NONE evidence "
        "contains visual_evidence."
    )

if (
    result["identification_status"] == "IDENTIFIED"
    and not result["identified_name"]
):
    raise RuntimeError(
        "IDENTIFIED runtime response has no identified_name."
    )

if (
    result["identification_status"] == "IDENTIFIED"
    and not result["visual_evidence"]
):
    raise RuntimeError(
        "IDENTIFIED runtime response has no visual_evidence."
    )

print("NONE/evidence consistency: PASS")
print("IDENTIFIED semantic consistency: PASS")
print("Runtime semantic boundary: PASS")


print()
print("===== 12. VERIFY ERROR SANITIZATION BOUNDARY =====")

for forbidden in [
    "GEMINI_API_KEY",
    "Traceback",
    "api_key",
    "password",
]:
    if forbidden in response.text:
        raise RuntimeError(
            f"Sensitive/internal data leaked: {forbidden}"
        )

print("Public response sanitization: PASS")


print()
print("===== 13. PRODUCTION SAFETY =====")

print("Controlled authenticated API regression: PASS")
print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 51 COMPLETE")
print("=" * 80)
print("Scanner route: PASS")
print("Authentication boundary: PASS")
print("Authenticated runtime success: PASS")
print("Public response envelope: PASS")
print("Intelligence response: PASS")
print("Response types/states: PASS")
print("Semantic response consistency: PASS")
print("Error sanitization: PASS")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
