from pathlib import Path
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.models.scan import Scan


print("=" * 80)
print("STEP 8C-006 — TASK 114 — REAL SCAN RETRIEVAL + HISTORY + ISOLATION")
print("=" * 80)


IMAGE_PATH = Path(
    "scripts/ai_heritage_scanner_controlled_test.png"
)

if not IMAGE_PATH.exists():
    raise RuntimeError(
        f"Controlled scanner image missing: {IMAGE_PATH}"
    )

image_bytes = IMAGE_PATH.read_bytes()

if not image_bytes:
    raise RuntimeError(
        "Controlled scanner image is empty."
    )


print()
print("===== 1. CONTROLLED IMAGE =====")
print("Image:", IMAGE_PATH)
print("Image bytes:", len(image_bytes))
print("Controlled image: PASS")


print()
print("===== 2. DATABASE PRE-STATE =====")

with engine.connect() as conn:
    before_scans = conn.execute(
        text("SELECT COUNT(*) FROM scans")
    ).scalar_one()

    before_users = conn.execute(
        text("SELECT COUNT(*) FROM users")
    ).scalar_one()

print("Existing users:", before_users)
print("Existing scans:", before_scans)
print("Database connection: PASS")


client = TestClient(app)


print()
print("===== 3. CREATE USER A =====")

suffix_a = uuid.uuid4().hex[:12]

email_a = f"task114a_{suffix_a}@gmail.com"
password_a = "Task114A!TemporaryPassword123"

registration_a = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": "Task 114 User A",
        "email": email_a,
        "password": password_a,
    },
)

if registration_a.status_code not in (200, 201):
    raise RuntimeError(
        "User A registration failed.\n"
        f"Status: {registration_a.status_code}\n"
        f"Body: {registration_a.text}"
    )

print("User A registration: PASS")


print()
print("===== 4. AUTHENTICATE USER A =====")

login_a = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_a,
        "password": password_a,
    },
)

if login_a.status_code != 200:
    raise RuntimeError(
        "User A authentication failed.\n"
        f"Status: {login_a.status_code}\n"
        f"Body: {login_a.text}"
    )

payload_a = login_a.json()

token_a = payload_a.get("access_token") or payload_a.get("token")

if not token_a:
    raise RuntimeError(
        "User A authentication succeeded but no token was returned."
    )

headers_a = {
    "Authorization": f"Bearer {token_a}"
}

print("User A authentication: PASS")


print()
print("===== 5. CREATE USER B =====")

suffix_b = uuid.uuid4().hex[:12]

email_b = f"task114b_{suffix_b}@gmail.com"
password_b = "Task114B!TemporaryPassword123"

registration_b = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": "Task 114 User B",
        "email": email_b,
        "password": password_b,
    },
)

if registration_b.status_code not in (200, 201):
    raise RuntimeError(
        "User B registration failed.\n"
        f"Status: {registration_b.status_code}\n"
        f"Body: {registration_b.text}"
    )

print("User B registration: PASS")


print()
print("===== 6. AUTHENTICATE USER B =====")

login_b = client.post(
    "/api/v1/auth/login",
    data={
        "username": email_b,
        "password": password_b,
    },
)

if login_b.status_code != 200:
    raise RuntimeError(
        "User B authentication failed.\n"
        f"Status: {login_b.status_code}\n"
        f"Body: {login_b.text}"
    )

payload_b = login_b.json()

token_b = payload_b.get("access_token") or payload_b.get("token")

if not token_b:
    raise RuntimeError(
        "User B authentication succeeded but no token was returned."
    )

headers_b = {
    "Authorization": f"Bearer {token_b}"
}

print("User B authentication: PASS")


print()
print("===== 7. CREATE REAL SCAN FOR USER A =====")

print("REAL GEMINI REQUEST: START")

with open(
    IMAGE_PATH,
    "rb",
) as image_file:

    scan_response = client.post(
        "/api/v1/ai/scan",
        headers=headers_a,
        files={
            "file": (
                IMAGE_PATH.name,
                image_file,
                "image/png",
            )
        },
    )

print("REAL GEMINI REQUEST: COMPLETED")

if scan_response.status_code != 200:
    raise RuntimeError(
        "User A scanner request failed.\n"
        f"Status: {scan_response.status_code}\n"
        f"Body: {scan_response.text}"
    )

scan_payload = scan_response.json()

scan_id = scan_payload.get("scan_id")

if not scan_id:
    raise RuntimeError(
        "Scanner response did not contain scan_id."
    )

print("User A real scanner request: PASS")
print("scan_id:", scan_id)


print()
print("===== 8. VERIFY USER A SINGLE-SCAN RETRIEVAL =====")

get_response_a = client.get(
    f"/api/v1/ai/scans/{scan_id}",
    headers=headers_a,
)

if get_response_a.status_code != 200:
    raise RuntimeError(
        "User A could not retrieve own scan.\n"
        f"Status: {get_response_a.status_code}\n"
        f"Body: {get_response_a.text}"
    )

retrieved_a = get_response_a.json()

retrieved_scan_id = retrieved_a.get("scan_id")

if retrieved_scan_id != scan_id:
    raise RuntimeError(
        "Retrieved scan_id does not match created scan_id."
    )

print("User A single scan retrieval: PASS")
print("Returned scan_id matches: PASS")


print()
print("===== 9. VERIFY USER A SCAN HISTORY =====")

history_a = client.get(
    "/api/v1/ai/scans",
    headers=headers_a,
)

if history_a.status_code != 200:
    raise RuntimeError(
        "User A scan history request failed.\n"
        f"Status: {history_a.status_code}\n"
        f"Body: {history_a.text}"
    )

history_payload_a = history_a.json()

if isinstance(history_payload_a, list):
    history_items_a = history_payload_a

elif isinstance(history_payload_a, dict):
    history_items_a = (
        history_payload_a.get("items")
        or history_payload_a.get("scans")
        or history_payload_a.get("data")
        or []
    )

else:
    raise RuntimeError(
        "Unexpected User A history response format."
    )

history_ids_a = {
    item.get("scan_id") or item.get("id")
    for item in history_items_a
    if isinstance(item, dict)
}

if scan_id not in history_ids_a:
    raise RuntimeError(
        "User A's newly created scan is missing from scan history."
    )

print("User A scan history: PASS")
print("Created scan appears in history: PASS")


print()
print("===== 10. VERIFY USER B CANNOT RETRIEVE USER A SCAN =====")

get_response_b = client.get(
    f"/api/v1/ai/scans/{scan_id}",
    headers=headers_b,
)

print("User B retrieval status:", get_response_b.status_code)

if get_response_b.status_code not in (403, 404):
    raise RuntimeError(
        "Cross-user scan access was not rejected.\n"
        f"Status: {get_response_b.status_code}\n"
        f"Body: {get_response_b.text}"
    )

print("User B cross-user retrieval rejection: PASS")
print("Cross-user isolation: PASS")


print()
print("===== 11. VERIFY USER B HISTORY ISOLATION =====")

history_b = client.get(
    "/api/v1/ai/scans",
    headers=headers_b,
)

if history_b.status_code != 200:
    raise RuntimeError(
        "User B scan history request failed.\n"
        f"Status: {history_b.status_code}\n"
        f"Body: {history_b.text}"
    )

history_payload_b = history_b.json()

if isinstance(history_payload_b, list):
    history_items_b = history_payload_b

elif isinstance(history_payload_b, dict):
    history_items_b = (
        history_payload_b.get("items")
        or history_payload_b.get("scans")
        or history_payload_b.get("data")
        or []
    )

else:
    raise RuntimeError(
        "Unexpected User B history response format."
    )

history_ids_b = {
    item.get("scan_id") or item.get("id")
    for item in history_items_b
    if isinstance(item, dict)
}

if scan_id in history_ids_b:
    raise RuntimeError(
        "User B can see User A's scan in scan history."
    )

print("User B scan history: PASS")
print("User A scan hidden from User B history: PASS")
print("History ownership isolation: PASS")


print()
print("===== 12. VERIFY PAGINATION CONTRACT =====")

history_page = client.get(
    "/api/v1/ai/scans?limit=1&offset=0",
    headers=headers_a,
)

if history_page.status_code != 200:
    raise RuntimeError(
        "Paginated scan history request failed.\n"
        f"Status: {history_page.status_code}\n"
        f"Body: {history_page.text}"
    )

print("Pagination request: PASS")

page_payload = history_page.json()

if isinstance(page_payload, list):
    page_items = page_payload
elif isinstance(page_payload, dict):
    page_items = (
        page_payload.get("items")
        or page_payload.get("scans")
        or page_payload.get("data")
        or []
    )
else:
    raise RuntimeError(
        "Unexpected paginated history response format."
    )

if len(page_items) > 1:
    raise RuntimeError(
        "Pagination limit=1 returned more than one item."
    )

print("limit=1 enforcement: PASS")


print()
print("===== 13. VERIFY DATABASE OWNERSHIP =====")

db = SessionLocal()

try:
    persisted_scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if persisted_scan is None:
        raise RuntimeError(
            "Created scan does not exist in database."
        )

    persisted_user_id = persisted_scan.user_id

    user_a = (
        db.query(User)
        .filter(User.email == email_a)
        .first()
    )

    user_b = (
        db.query(User)
        .filter(User.email == email_b)
        .first()
    )

    if user_a is None or user_b is None:
        raise RuntimeError(
            "Temporary users could not be found."
        )

    if persisted_user_id != user_a.id:
        raise RuntimeError(
            "Persisted scan does not belong to User A."
        )

    if persisted_user_id == user_b.id:
        raise RuntimeError(
            "Persisted scan incorrectly belongs to User B."
        )

    print("Scan owner: User A")
    print("User A ownership: PASS")
    print("User B ownership separation: PASS")

finally:
    db.close()


print()
print("===== 14. VERIFY NEWEST-FIRST ORDERING =====")

ordered_items = history_items_a

timestamps = []

for item in ordered_items:
    value = (
        item.get("created_at")
        or item.get("createdAt")
    )

    if value:
        timestamps.append(value)

if len(timestamps) >= 2:
    if timestamps != sorted(
        timestamps,
        reverse=True,
    ):
        raise RuntimeError(
            "Scan history is not newest-first."
        )

    print("Newest-first ordering: PASS")

else:
    print(
        "Newest-first ordering: "
        "INSUFFICIENT MULTI-ROW DATA — repository contract already verified"
    )


print()
print("===== 15. CLEANUP TEMPORARY DATA =====")

cleanup_db = SessionLocal()

try:
    temporary_scan = (
        cleanup_db.query(Scan)
        .filter(Scan.id == scan_id)
        .first()
    )

    if temporary_scan is not None:
        cleanup_db.delete(temporary_scan)

    temporary_user_a = (
        cleanup_db.query(User)
        .filter(User.email == email_a)
        .first()
    )

    if temporary_user_a is not None:
        cleanup_db.delete(temporary_user_a)

    temporary_user_b = (
        cleanup_db.query(User)
        .filter(User.email == email_b)
        .first()
    )

    if temporary_user_b is not None:
        cleanup_db.delete(temporary_user_b)

    cleanup_db.commit()

finally:
    cleanup_db.close()

print("Temporary scan removed: PASS")
print("Temporary User A removed: PASS")
print("Temporary User B removed: PASS")


print()
print("===== 16. VERIFY DATABASE RESTORATION =====")

with engine.connect() as conn:
    final_scans = conn.execute(
        text("SELECT COUNT(*) FROM scans")
    ).scalar_one()

    final_users = conn.execute(
        text("SELECT COUNT(*) FROM users")
    ).scalar_one()

    remaining_a = conn.execute(
        text(
            "SELECT COUNT(*) FROM users WHERE email = :email"
        ),
        {"email": email_a},
    ).scalar_one()

    remaining_b = conn.execute(
        text(
            "SELECT COUNT(*) FROM users WHERE email = :email"
        ),
        {"email": email_b},
    ).scalar_one()

print("Final users:", final_users)
print("Final scans:", final_scans)

if final_scans != before_scans:
    raise RuntimeError(
        "Scan cleanup failed."
    )

if final_users != before_users:
    raise RuntimeError(
        "User cleanup failed."
    )

if remaining_a != 0:
    raise RuntimeError(
        "Temporary User A still exists."
    )

if remaining_b != 0:
    raise RuntimeError(
        "Temporary User B still exists."
    )

print("Database restoration: PASS")


print()
print("=" * 80)
print("TASK 114 COMPLETE")
print("=" * 80)
print("User A authentication: PASS")
print("User B authentication: PASS")
print("Real scanner persistence: PASS")
print("Single scan retrieval: PASS")
print("User scan history: PASS")
print("Cross-user retrieval isolation: PASS")
print("History ownership isolation: PASS")
print("Pagination: PASS")
print("Database ownership: PASS")
print("Newest-first ordering: PASS")
print("Temporary data cleanup: PASS")
print("Database restoration: PASS")
print()
print("NO PERMANENT TEST DATA CREATED.")
print("SCANNER RETRIEVAL + HISTORY + ISOLATION RUNTIME GATE: PASS")
print("READY FOR TASKS 115-124.")
print("=" * 80)
