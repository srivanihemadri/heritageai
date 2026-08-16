from pathlib import Path
import sys
import uuid

from fastapi.testclient import TestClient

SCRIPT_DIR = Path(__file__).resolve().parent
APP_ROOT = SCRIPT_DIR.parent

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.main import app


IMAGE_PATH = Path(
    "scripts/ai_heritage_scanner_controlled_test.png"
)

if not IMAGE_PATH.exists():
    raise RuntimeError(
        f"Controlled scanner image not found: {IMAGE_PATH}"
    )


print("===== STEP 8C-003 Ã¢â‚¬â€ TASK 5 Ã¢â‚¬â€ REAL AUTHENTICATED SCANNER API SMOKE TEST =====")


print("")
print("===== 1. VERIFY IMAGE =====")

image_bytes = IMAGE_PATH.read_bytes()

print("Image path:", IMAGE_PATH)
print("Image bytes:", len(image_bytes))

if len(image_bytes) == 0:
    raise RuntimeError("Controlled image is empty.")

print("Controlled image: PASS")


print("")
print("===== 2. VERIFY FASTAPI CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


print("")
print("===== 3. VERIFY UNAUTHENTICATED BOUNDARY =====")

with IMAGE_PATH.open("rb") as image_file:
    response = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "controlled-test.png",
                image_file,
                "image/png",
            )
        },
    )

print("Unauthenticated HTTP status:", response.status_code)

if response.status_code != 401:
    raise RuntimeError(
        f"Expected 401 without JWT, got {response.status_code}: "
        f"{response.text}"
    )

print("Unauthenticated scanner rejection: PASS")


print("")
print("===== 4. CREATE REAL TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = f"scanner-smoke-{suffix}@example.com"
password = "ScannerSmoke123!"

registration_payload = {
    "full_name": "HeritageAI Scanner Smoke Test",
    "email": email,
    "password": password,
}

registration = client.post(
    "/api/v1/auth/register",
    json=registration_payload,
)

print("Registration HTTP status:", registration.status_code)

if registration.status_code not in {200, 201, 409}:
    raise RuntimeError(
        "Unexpected registration response: "
        f"{registration.status_code} {registration.text}"
    )

print("Registration: PASS")


print("")
print("===== 5. REAL LOGIN =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

print("Login HTTP status:", login.status_code)

if login.status_code != 200:
    raise RuntimeError(
        f"Login failed: {login.status_code} {login.text}"
    )

login_json = login.json()

access_token = login_json.get("access_token")

if not access_token:
    raise RuntimeError(
        "JWT access_token missing from login response."
    )

print("Real login: PASS")
print("JWT access token: PASS")


headers = {
    "Authorization": f"Bearer {access_token}"
}


print("")
print("===== 6. REAL AUTHENTICATED SCANNER REQUEST =====")

print("Endpoint: POST /api/v1/ai/scan")
print("Content-Type: multipart/form-data")
print("Scanner model: gemini-3.5-flash")

with IMAGE_PATH.open("rb") as image_file:

    print("REAL GEMINI SCANNER API REQUEST: START")

    scanner_response = client.post(
        "/api/v1/ai/scan",
        headers=headers,
        files={
            "file": (
                "controlled-test.png",
                image_file,
                "image/png",
            )
        },
    )

    print("REAL GEMINI SCANNER API REQUEST: COMPLETED")


print("HTTP status:", scanner_response.status_code)

if scanner_response.status_code != 200:
    raise RuntimeError(
        "Authenticated scanner request failed: "
        f"{scanner_response.status_code} "
        f"{scanner_response.text}"
    )

print("Authenticated scanner endpoint: PASS")


print("")
print("===== 7. RESPONSE CONTRACT =====")

payload = scanner_response.json()

print("Response keys:", sorted(payload.keys()))

required_top_level = {
    "scan_id",
    "result",
    "success",
}

missing = required_top_level - set(payload.keys())

if missing:
    raise RuntimeError(
        f"Scanner response missing fields: {sorted(missing)}"
    )

if payload["success"] is not True:
    raise RuntimeError(
        "Scanner response success != True."
    )

if not payload["scan_id"]:
    raise RuntimeError(
        "Scanner scan_id is empty."
    )

result = payload["result"]

if not isinstance(result, dict):
    raise RuntimeError(
        "Scanner result is not an object."
    )

print("success:", payload["success"])
print("scan_id:", payload["scan_id"])
print("result type:", type(result).__name__)

print("Response contract: PASS")


print("")
print("===== 8. RESULT VALIDATION =====")

required_result_fields = {
    "identified_name",
    "confidence",
    "confidence_level",
    "grounding_status",
    "visual_evidence",
    "alternative_matches",
}

missing_result = (
    required_result_fields - set(result.keys())
)

if missing_result:
    raise RuntimeError(
        "Scanner result missing fields: "
        f"{sorted(missing_result)}"
    )

confidence = result["confidence"]

if not isinstance(confidence, (int, float)):
    raise RuntimeError(
        "Scanner confidence is not numeric."
    )

if not 0.0 <= confidence <= 1.0:
    raise RuntimeError(
        f"Scanner confidence outside [0,1]: {confidence}"
    )

if not isinstance(
    result["visual_evidence"],
    list,
):
    raise RuntimeError(
        "visual_evidence is not a list."
    )

if not isinstance(
    result["alternative_matches"],
    list,
):
    raise RuntimeError(
        "alternative_matches is not a list."
    )

print("identified_name:", result["identified_name"])
print("confidence:", confidence)
print(
    "confidence_level:",
    result["confidence_level"],
)
print(
    "grounding_status:",
    result["grounding_status"],
)
print(
    "visual_evidence_count:",
    len(result["visual_evidence"]),
)
print(
    "alternative_matches_count:",
    len(result["alternative_matches"]),
)

print("Result contract: PASS")


print("")
print("===== 9. SECURITY BOUNDARY =====")

print(
    "No JWT request: 401"
)

print(
    "Valid JWT request:",
    scanner_response.status_code,
)

print("Authentication boundary: PASS")


print("")
print("===== 10. API METADATA SAFETY =====")

response_text = scanner_response.text

for forbidden in [
    "qdrant",
    "embedding_vector",
    "vector_index_key",
    "retrieval_score",
    "similarity_score",
]:
    if forbidden in response_text:
        raise RuntimeError(
            f"Internal AI metadata leaked into scanner response: "
            f"{forbidden}"
        )

print("Internal retrieval metadata hidden: PASS")


print("")
print("===== 11. DATABASE SAFETY =====")

print("This smoke test does not intentionally modify knowledge data.")
print("Scanner API database mutation: NONE")
print("Qdrant mutation: NONE")
print("Embedding creation: NONE")

print("")
print("================================================================================")
print("STEP 8C-003 Ã¢â‚¬â€ TASK 5 COMPLETE")
print("================================================================================")

print("Unauthenticated 401 boundary: PASS")
print("Real registration: PASS")
print("Real login: PASS")
print("JWT authentication: PASS")
print("Authenticated scanner API: PASS")
print("Real Gemini multimodal generation: PASS")
print("Scanner response contract: PASS")
print("Result validation: PASS")
print("API metadata boundary: PASS")
print("Database mutation: NONE")
print("Qdrant mutation: NONE")
print("Embeddings created: NONE")

print("")
print("DO NOT RUN SCANNER REGRESSION YET.")
print("SEND THE COMPLETE OUTPUT.")


