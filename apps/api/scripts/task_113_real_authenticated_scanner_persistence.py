from pathlib import Path
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from app.main import app
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.models.scan import Scan


print("=" * 80)
print("STEP 8C-006 — TASK 113 — REAL AUTHENTICATED SCANNER PERSISTENCE")
print("=" * 80)

IMAGE_PATH = Path(
    "scripts/ai_heritage_scanner_controlled_test.png"
)

if not IMAGE_PATH.exists():
    raise RuntimeError(
        f"Controlled scanner image missing: {IMAGE_PATH}"
    )

image_bytes = IMAGE_PATH.read_bytes()

print()
print("===== 1. CONTROLLED IMAGE =====")
print("Image:", IMAGE_PATH)
print("Image bytes:", len(image_bytes))

if not image_bytes:
    raise RuntimeError("Scanner image is empty.")

print("Controlled image: PASS")


print()
print("===== 2. DATABASE PRE-STATE =====")

with engine.connect() as conn:
    before_scans = conn.execute(
        text("SELECT COUNT(*) FROM scans")
    ).scalar_one()

print("Existing scans before test:", before_scans)
print("Database connection: PASS")


print()
print("===== 3. CREATE TEMPORARY AUTHENTICATED USER =====")

suffix = uuid.uuid4().hex[:12]

email = f"task113_{suffix}@gmail.com"
password = "Task113!TemporaryPassword123"

client = TestClient(app)

registration_response = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": "Task 113 Runtime User",
        "email": email,
        "password": password,
    },
)

if registration_response.status_code not in (200, 201):
    raise RuntimeError(
        "Temporary user registration failed.\n"
        f"Status: {registration_response.status_code}\n"
        f"Body: {registration_response.text}"
    )

print("Temporary user registration: PASS")


print()
print("===== 4. AUTHENTICATE TEMPORARY USER =====")

login_response = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login_response.status_code != 200:
    raise RuntimeError(
        "Temporary user authentication failed.\n"
        f"Status: {login_response.status_code}\n"
        f"Body: {login_response.text}"
    )

login_payload = login_response.json()

token = login_payload.get("access_token")

if not token:
    token = login_payload.get("token")

if not token:
    raise RuntimeError(
        "Authentication succeeded but no access token was returned."
    )

print("Authentication: PASS")


print()
print("===== 5. REAL AUTHENTICATED SCANNER REQUEST =====")

print("REAL GEMINI REQUEST: START")

with open(
    IMAGE_PATH,
    "rb",
) as image_file:

    scanner_response = client.post(
        "/api/v1/ai/scan",
        headers={
            "Authorization": f"Bearer {token}",
        },
        files={
            "file": (
                IMAGE_PATH.name,
                image_file,
                "image/png",
            )
        },
    )

print("REAL GEMINI REQUEST: COMPLETED")

if scanner_response.status_code != 200:
    raise RuntimeError(
        "Real authenticated scanner request failed.\n"
        f"Status: {scanner_response.status_code}\n"
        f"Body: {scanner_response.text}"
    )

payload = scanner_response.json()

print("HTTP status: 200")
print("Scanner response JSON: PASS")


print()
print("===== 6. VERIFY PUBLIC SCAN CONTRACT =====")

if payload.get("success") is not True:
    raise RuntimeError(
        "Scanner response success flag is not true."
    )

scan_id = payload.get("scan_id")
result = payload.get("result")

if not scan_id:
    raise RuntimeError(
        "Scanner response did not contain scan_id."
    )

if not isinstance(result, dict):
    raise RuntimeError(
        "Scanner response result is not an object."
    )

print("success: PASS")
print("scan_id:", scan_id)
print("result: PASS")
print("Stable scan response: PASS")


print()
print("===== 7. VERIFY REQUIRED RESULT DATA =====")

required_fields = [
    "identification_status",
    "evidence_quality",
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
]

for field in required_fields:
    if field not in result:
        raise RuntimeError(
            f"Scanner result field missing: {field}"
        )

    print(f"{field}: PRESENT")

print("Scanner result contract: PASS")


print()
print("===== 8. VERIFY DATABASE PERSISTENCE =====")

db = SessionLocal()

try:
    persisted = (
        db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if persisted is None:
        raise RuntimeError(
            "Scanner returned scan_id but no database record exists."
        )

    print("Persisted Scan entity: PRESENT")

    if persisted.user_id is None:
        raise RuntimeError(
            "Persisted scan has no user ownership."
        )

    print("user_id: PRESENT")

    checks = [
        (
            "identification_status",
            persisted.identification_status,
            result["identification_status"],
        ),
        (
            "evidence_quality",
            persisted.evidence_quality,
            result["evidence_quality"],
        ),
        (
            "confidence",
            persisted.confidence,
            result["confidence"],
        ),
        (
            "confidence_level",
            persisted.confidence_level,
            result["confidence_level"],
        ),
        (
            "visual_evidence",
            persisted.visual_evidence,
            result["visual_evidence"],
        ),
        (
            "alternative_matches",
            persisted.alternative_matches,
            result["alternative_matches"],
        ),
    ]

    for field, actual, expected in checks:
        if actual != expected:
            raise RuntimeError(
                f"Persisted {field} does not match API result."
            )

    if persisted.created_at is None:
        raise RuntimeError(
            "Persisted created_at is missing."
        )

    if persisted.updated_at is None:
        raise RuntimeError(
            "Persisted updated_at is missing."
        )

    print("Result mapping: PASS")
    print("created_at: PRESENT")
    print("updated_at: PRESENT")
    print("Database persistence: PASS")

finally:
    db.close()


print()
print("===== 9. VERIFY NO RAW IMAGE PERSISTENCE =====")

columns = {
    column["name"]
    for column in inspect(engine).get_columns("scans")
}

forbidden_columns = {
    "image_bytes",
    "image_base64",
    "raw_image",
    "raw_response",
}

present_forbidden = columns.intersection(
    forbidden_columns
)

if present_forbidden:
    raise RuntimeError(
        f"Forbidden persistence columns found: {present_forbidden}"
    )

print("Raw image persistence columns: NOT PRESENT")
print("Raw Gemini response persistence columns: NOT PRESENT")
print("Persistence safety: PASS")


print()
print("===== 10. VERIFY SCAN COUNT INCREASE =====")

with engine.connect() as conn:
    after_scans = conn.execute(
        text("SELECT COUNT(*) FROM scans")
    ).scalar_one()

print("Scans before:", before_scans)
print("Scans after:", after_scans)

if after_scans != before_scans + 1:
    raise RuntimeError(
        "Expected exactly one persisted scan."
    )

print("Scan count increase: PASS")


print()
print("===== 11. CLEANUP TEMPORARY TEST DATA =====")

cleanup_db = SessionLocal()

try:
    temporary_scan = (
        cleanup_db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if temporary_scan is not None:
        cleanup_db.delete(temporary_scan)

    temporary_user = (
        cleanup_db.query(User)
        .filter(User.email == email)
        .first()
    )

    if temporary_user is not None:
        cleanup_db.delete(temporary_user)

    cleanup_db.commit()

finally:
    cleanup_db.close()

print("Temporary scan removed: PASS")
print("Temporary user removed: PASS")


print()
print("===== 12. VERIFY CLEAN DATABASE STATE =====")

with engine.connect() as conn:
    final_scans = conn.execute(
        text("SELECT COUNT(*) FROM scans")
    ).scalar_one()

    remaining_user = conn.execute(
        text(
            "SELECT COUNT(*) FROM users WHERE email = :email"
        ),
        {"email": email},
    ).scalar_one()

print("Final scans:", final_scans)

if final_scans != before_scans:
    raise RuntimeError(
        "Cleanup failed: scan count did not return to original state."
    )

if remaining_user != 0:
    raise RuntimeError(
        "Cleanup failed: temporary user still exists."
    )

print("Database cleanup: PASS")


print()
print("=" * 80)
print("TASK 113 COMPLETE")
print("=" * 80)
print("Authentication: PASS")
print("Real Gemini request: PASS")
print("Scanner JSON parsing: PASS")
print("Scanner contract validation: PASS")
print("scan_id generation: PASS")
print("Repository persistence: PASS")
print("Database commit: PASS")
print("Persisted result verification: PASS")
print("Persistence safety: PASS")
print("Temporary data cleanup: PASS")
print()
print("NO PERMANENT TEST DATA CREATED.")
print("READY FOR TASK 114 — RETRIEVAL + HISTORY + CROSS-USER ISOLATION")
print("=" * 80)

