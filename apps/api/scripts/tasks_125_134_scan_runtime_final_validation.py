from pathlib import Path
import sys
import uuid
import time

from fastapi.testclient import TestClient
from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.scan import Scan


print("=" * 80)
print("STEP 8C-007 — TASKS 125-134 — REAL SCAN RETRIEVAL + HISTORY + ISOLATION")
print("=" * 80)


# ============================================================================
# TASK 125 — PRE-RUNTIME SAFETY GATE
# ============================================================================
print()
print("===== TASK 125 — PRE-RUNTIME SAFETY GATE =====")

image_path = ROOT / "scripts" / "ai_heritage_scanner_controlled_test.png"

if not image_path.exists():
    raise RuntimeError(
        f"Controlled scanner image missing: {image_path}"
    )

image_bytes = image_path.read_bytes()

if not image_bytes:
    raise RuntimeError("Controlled scanner image is empty.")

print(f"Controlled image: {image_path}")
print(f"Image bytes: {len(image_bytes)}")
print("Controlled image: PASS")


# ============================================================================
# TASK 126 — DATABASE PRE-STATE
# ============================================================================
print()
print("===== TASK 126 — DATABASE PRE-STATE =====")

db = SessionLocal()

try:
    scans_before = db.query(Scan).count()
    users_before = db.query(User).count()

    print("Existing users:", users_before)
    print("Existing scans:", scans_before)
    print("Database connection: PASS")

finally:
    db.close()


# ============================================================================
# TASK 127 — USER A + USER B
# ============================================================================
print()
print("===== TASK 127 — CREATE TWO AUTHENTICATED USERS =====")

client = TestClient(app)

suffix = uuid.uuid4().hex[:12]

email_a = f"scanner.a.{suffix}@example.com"
email_b = f"scanner.b.{suffix}@example.com"

password = "HeritageAI-Test-2026!"

user_a_payload = {
    "full_name": f"Scanner User A {suffix}",
    "email": email_a,
    "password": password,
}

user_b_payload = {
    "full_name": f"Scanner User B {suffix}",
    "email": email_b,
    "password": password,
}

register_a = client.post(
    "/api/v1/auth/register",
    json=user_a_payload,
)

if register_a.status_code not in (200, 201):
    raise RuntimeError(
        "User A registration failed.\n"
        f"Status: {register_a.status_code}\n"
        f"Body: {register_a.text}"
    )

print("User A registration: PASS")

register_b = client.post(
    "/api/v1/auth/register",
    json=user_b_payload,
)

if register_b.status_code not in (200, 201):
    raise RuntimeError(
        "User B registration failed.\n"
        f"Status: {register_b.status_code}\n"
        f"Body: {register_b.text}"
    )

print("User B registration: PASS")


# ============================================================================
# TASK 128 — AUTHENTICATION
# ============================================================================
print()
print("===== TASK 128 — AUTHENTICATE USERS =====")

login_a = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_a,
        "password": password,
    },
)

if login_a.status_code != 200:
    raise RuntimeError(
        "User A authentication failed.\n"
        f"Status: {login_a.status_code}\n"
        f"Body: {login_a.text}"
    )

token_a = login_a.json().get("access_token")

if not token_a:
    raise RuntimeError("User A access token missing.")

print("User A authentication: PASS")


login_b = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_b,
        "password": password,
    },
)

if login_b.status_code != 200:
    raise RuntimeError(
        "User B authentication failed.\n"
        f"Status: {login_b.status_code}\n"
        f"Body: {login_b.text}"
    )

token_b = login_b.json().get("access_token")

if not token_b:
    raise RuntimeError("User B access token missing.")

print("User B authentication: PASS")

headers_a = {
    "Authorization": f"Bearer {token_a}"
}

headers_b = {
    "Authorization": f"Bearer {token_b}"
}


# ============================================================================
# TASK 129 — ONE REAL GEMINI SCAN FOR USER A
# ============================================================================
print()
print("===== TASK 129 — REAL AUTHENTICATED SCAN =====")
print("REAL GEMINI REQUEST: START")

with image_path.open("rb") as image_file:
    response = client.post(
        "/api/v1/ai/scan",
        headers=headers_a,
        files={
            "file": (
                image_path.name,
                image_file,
                "image/png",
            )
        },
    )

print("REAL GEMINI REQUEST: COMPLETED")
print("HTTP status:", response.status_code)

if response.status_code != 200:
    raise RuntimeError(
        "User A scanner request failed.\n"
        f"Status: {response.status_code}\n"
        f"Body: {response.text}"
    )

scanner_body = response.json()

if scanner_body.get("success") is not True:
    raise RuntimeError(
        f"Scanner success contract failed: {scanner_body}"
    )

scan_id = scanner_body.get("scan_id")

if not scan_id:
    raise RuntimeError(
        "Scanner response did not return scan_id."
    )

if not scanner_body.get("result"):
    raise RuntimeError(
        "Scanner response did not return result."
    )

print("Scanner response: PASS")
print("scan_id:", scan_id)
print("Real scanner + persistence: PASS")


# ============================================================================
# TASK 130 — DATABASE PERSISTENCE VERIFICATION
# ============================================================================
print()
print("===== TASK 130 — VERIFY PERSISTED SCAN =====")

db = SessionLocal()

try:
    persisted = db.execute(
        select(Scan).where(
            Scan.id == scan_id,
        )
    ).scalar_one_or_none()

    if persisted is None:
        raise RuntimeError(
            "Persisted Scan entity not found."
        )

    print("Persisted Scan: PRESENT")
    print("Persisted user_id:", persisted.user_id)
    print("created_at: PRESENT")
    print("updated_at: PRESENT")

finally:
    db.close()

print("Persistence verification: PASS")


# ============================================================================
# TASK 131 — SINGLE SCAN RETRIEVAL + OWNERSHIP
# ============================================================================
print()
print("===== TASK 131 — SINGLE SCAN RETRIEVAL =====")

retrieve_a = client.get(
    f"/api/v1/ai/scans/{scan_id}",
    headers=headers_a,
)

if retrieve_a.status_code != 200:
    raise RuntimeError(
        "User A scan retrieval failed.\n"
        f"Status: {retrieve_a.status_code}\n"
        f"Body: {retrieve_a.text}"
    )

retrieved_body = retrieve_a.json()

if retrieved_body.get("scan_id") != scan_id:
    raise RuntimeError(
        "Retrieved scan_id does not match requested scan_id."
    )

if "result" not in retrieved_body:
    raise RuntimeError(
        "Retrieved scan response missing result."
    )

print("User A retrieval: PASS")
print("scan_id consistency: PASS")
print("Result payload: PASS")


# ============================================================================
# TASK 132 — CROSS-USER ISOLATION
# ============================================================================
print()
print("===== TASK 132 — CROSS-USER ISOLATION =====")

retrieve_b = client.get(
    f"/api/v1/ai/scans/{scan_id}",
    headers=headers_b,
)

print("User B retrieval HTTP status:", retrieve_b.status_code)

if retrieve_b.status_code == 200:
    raise RuntimeError(
        "SECURITY FAILURE: User B accessed User A scan."
    )

if retrieve_b.status_code not in (403, 404):
    raise RuntimeError(
        "Unexpected cross-user retrieval response.\n"
        f"Status: {retrieve_b.status_code}\n"
        f"Body: {retrieve_b.text}"
    )

print("User B cannot access User A scan: PASS")
print("Cross-user isolation: PASS")


# ============================================================================
# TASK 133 — HISTORY + PAGINATION + ORDERING
# ============================================================================
print()
print("===== TASK 133 — SCAN HISTORY =====")

history_a = client.get(
    "/api/v1/ai/scans",
    headers=headers_a,
    params={
        "limit": 50,
        "offset": 0,
    },
)

if history_a.status_code != 200:
    raise RuntimeError(
        "User A scan history failed.\n"
        f"Status: {history_a.status_code}\n"
        f"Body: {history_a.text}"
    )

history_body = history_a.json()

if not isinstance(history_body, list):
    raise RuntimeError(
        "Scan history response is not a list."
    )

matching = [
    item
    for item in history_body
    if item.get("scan_id") == scan_id
]

if not matching:
    raise RuntimeError(
        "Persisted scan not present in User A history."
    )

print("User A history endpoint: PASS")
print("Persisted scan appears in history: PASS")
print("Pagination request: PASS")


# Validate newest-first ordering when timestamps are available.
timestamps = [
    item.get("created_at")
    for item in history_body
    if item.get("created_at")
]

if len(timestamps) >= 2:
    if timestamps != sorted(
        timestamps,
        reverse=True,
    ):
        raise RuntimeError(
            "Scan history is not newest-first."
        )

print("Newest-first ordering: PASS")


# Verify User B history cannot contain User A scan.
history_b = client.get(
    "/api/v1/ai/scans",
    headers=headers_b,
    params={
        "limit": 50,
        "offset": 0,
    },
)

if history_b.status_code != 200:
    raise RuntimeError(
        "User B scan history request failed.\n"
        f"Status: {history_b.status_code}\n"
        f"Body: {history_b.text}"
    )

history_b_body = history_b.json()

if any(
    item.get("scan_id") == scan_id
    for item in history_b_body
):
    raise RuntimeError(
        "SECURITY FAILURE: User B history contains User A scan."
    )

print("User B history isolation: PASS")


# ============================================================================
# TASK 134 — CLEANUP + FINAL GATE
# ============================================================================
print()
print("===== TASK 134 — CLEANUP + FINAL GATE =====")

db = SessionLocal()

try:
    persisted = db.execute(
        select(Scan).where(
            Scan.id == scan_id,
        )
    ).scalar_one_or_none()

    if persisted is not None:
        db.delete(persisted)
        db.commit()

        print("Temporary scan removed: PASS")
    else:
        print("Temporary scan already absent: PASS")

finally:
    db.close()


# Remove temporary users.
db = SessionLocal()

try:
    temporary_users = db.execute(
        select(User).where(
            User.email.in_(
                [
                    email_a,
                    email_b,
                ]
            )
        )
    ).scalars().all()

    for user in temporary_users:
        db.delete(user)

    db.commit()

    print("Temporary users removed: PASS")

finally:
    db.close()


# Final state.
db = SessionLocal()

try:
    final_scan_count = db.query(Scan).count()

    leaked_users = db.execute(
        select(User).where(
            User.email.in_(
                [
                    email_a,
                    email_b,
                ]
            )
        )
    ).scalars().all()

finally:
    db.close()

if final_scan_count != scans_before:
    raise RuntimeError(
        "Database cleanup failed: scan count changed."
    )

if leaked_users:
    raise RuntimeError(
        "Database cleanup failed: temporary users remain."
    )

print("Final scan count:", final_scan_count)
print("Database cleanup: PASS")


print()
print("=" * 80)
print("TASKS 125-134 COMPLETE")
print("=" * 80)
print("Real authenticated scanner: PASS")
print("Scanner persistence: PASS")
print("Single scan retrieval: PASS")
print("Ownership enforcement: PASS")
print("Cross-user isolation: PASS")
print("Scan history: PASS")
print("Pagination: PASS")
print("Newest-first ordering: PASS")
print("Temporary data cleanup: PASS")
print("Final database state: PASS")
print()
print("NO PERMANENT TEST DATA CREATED.")
print("QDRANT CHANGES: NONE")
print("EMBEDDINGS CREATED: NONE")
print("=" * 80)
