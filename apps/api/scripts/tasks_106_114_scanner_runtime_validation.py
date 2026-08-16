from pathlib import Path
import sys
import time
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import func, select

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.scan import Scan


print("=" * 80)
print("STEP 8C-006 — TASKS 106-114 — REAL SCANNER PERSISTENCE RUNTIME VALIDATION")
print("=" * 80)


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

IMAGE_PATH = APP_ROOT / "scripts" / "ai_heritage_scanner_controlled_test.png"

if not IMAGE_PATH.exists():
    raise RuntimeError(
        f"Controlled scanner image not found: {IMAGE_PATH}"
    )

TEST_SUFFIX = uuid.uuid4().hex[:12]

USER_A_EMAIL = (
    f"heritageai.runtime.a.{TEST_SUFFIX}@example.com"
)

USER_B_EMAIL = (
    f"heritageai.runtime.b.{TEST_SUFFIX}@example.com"
)

TEST_PASSWORD = "HeritageAI_Runtime_2026_Test!"

USER_A_ID = None
USER_B_ID = None
SCAN_ID = None

client = TestClient(app)


def register_user(email: str, full_name: str):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": TEST_PASSWORD,
        },
    )

    if response.status_code != 201:
        raise RuntimeError(
            "Registration failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    payload = response.json()

    if not payload.get("success"):
        raise RuntimeError(
            f"Registration returned unsuccessful response: {payload}"
        )

    return payload


def login_user(email: str):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": TEST_PASSWORD,
        },
    )

    if response.status_code != 200:
        raise RuntimeError(
            "Login failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    payload = response.json()

    token = payload.get("access_token")

    if not token:
        raise RuntimeError(
            f"Login response did not contain access_token: {payload}"
        )

    return token


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
    }


try:

    # =======================================================================
    # TASK 106 — DATABASE RUNTIME CONNECTIVITY
    # =======================================================================

    print()
    print("===== TASK 106 — DATABASE RUNTIME CONNECTIVITY =====")

    db = SessionLocal()

    try:
        user_count = db.scalar(
            select(func.count()).select_from(User)
        )

        scan_count = db.scalar(
            select(func.count()).select_from(Scan)
        )

        print("Database connection: PASS")
        print(f"Existing users: {user_count}")
        print(f"Existing scans: {scan_count}")

    finally:
        db.close()


    # =======================================================================
    # TASK 107 — AUTHENTICATED USER A
    # =======================================================================

    print()
    print("===== TASK 107 — AUTHENTICATED USER A =====")

    register_user(
        USER_A_EMAIL,
        "HeritageAI Runtime User A",
    )

    token_a = login_user(USER_A_EMAIL)

    print("User A registration: PASS")
    print("User A authentication: PASS")


    # =======================================================================
    # TASK 108 — AUTHENTICATED USER B
    # =======================================================================

    print()
    print("===== TASK 108 — AUTHENTICATED USER B =====")

    register_user(
        USER_B_EMAIL,
        "HeritageAI Runtime User B",
    )

    token_b = login_user(USER_B_EMAIL)

    print("User B registration: PASS")
    print("User B authentication: PASS")


    # =======================================================================
    # TASK 109 — REAL SCANNER REQUEST
    # =======================================================================

    print()
    print("===== TASK 109 — REAL GEMINI SCANNER REQUEST =====")

    image_bytes = IMAGE_PATH.read_bytes()

    if not image_bytes:
        raise RuntimeError("Controlled scanner image is empty.")

    print(f"Scanner image bytes: {len(image_bytes)}")

    with IMAGE_PATH.open("rb") as image_file:

        response = client.post(
            "/api/v1/ai/scan",
            headers=auth_headers(token_a),
            files={
                "file": (
                    IMAGE_PATH.name,
                    image_file,
                    "image/png",
                )
            },
        )

    print("HTTP status:", response.status_code)

    if response.status_code != 200:
        raise RuntimeError(
            "Real scanner request failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    scanner_payload = response.json()

    if scanner_payload.get("success") is not True:
        raise RuntimeError(
            f"Scanner response success flag invalid: {scanner_payload}"
        )

    SCAN_ID = scanner_payload.get("scan_id")

    if not SCAN_ID:
        raise RuntimeError(
            f"Scanner response did not contain scan_id: {scanner_payload}"
        )

    if not scanner_payload.get("result"):
        raise RuntimeError(
            f"Scanner response did not contain result: {scanner_payload}"
        )

    print("Real Gemini scanner request: PASS")
    print("Scanner response: PASS")
    print("scan_id:", SCAN_ID)


    # =======================================================================
    # TASK 110 — DATABASE PERSISTENCE VERIFICATION
    # =======================================================================

    print()
    print("===== TASK 110 — DATABASE PERSISTENCE VERIFICATION =====")

    db = SessionLocal()

    try:

        persisted_scan = db.execute(
            select(Scan).where(
                Scan.id == SCAN_ID,
            )
        ).scalar_one_or_none()

        if persisted_scan is None:
            raise RuntimeError(
                "Scanner returned scan_id but no database record was found."
            )

        USER_A_ID = persisted_scan.user_id

        print("Persisted scan: PASS")
        print("Persisted user_id:", USER_A_ID)
        print("Persisted scan_id:", persisted_scan.id)
        print("Identification status:", persisted_scan.identification_status)
        print("Evidence quality:", persisted_scan.evidence_quality)
        print("Confidence:", persisted_scan.confidence)
        print("Grounding status:", persisted_scan.grounding_status)

    finally:
        db.close()


    # =======================================================================
    # TASK 111 — SINGLE SCAN RETRIEVAL
    # =======================================================================

    print()
    print("===== TASK 111 — SINGLE SCAN RETRIEVAL =====")

    response = client.get(
        f"/api/v1/ai/scans/{SCAN_ID}",
        headers=auth_headers(token_a),
    )

    if response.status_code != 200:
        raise RuntimeError(
            "Single scan retrieval failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    retrieved = response.json()

    if retrieved.get("scan_id") != SCAN_ID:
        raise RuntimeError(
            "Retrieved scan_id does not match persisted scan."
        )

    if retrieved.get("success") is not True:
        raise RuntimeError(
            f"Single scan response unsuccessful: {retrieved}"
        )

    print("Single scan retrieval: PASS")


    # =======================================================================
    # TASK 112 — SCAN HISTORY + PAGINATION
    # =======================================================================

    print()
    print("===== TASK 112 — SCAN HISTORY + PAGINATION =====")

    response = client.get(
        "/api/v1/ai/scans",
        params={
            "limit": 10,
            "offset": 0,
        },
        headers=auth_headers(token_a),
    )

    if response.status_code != 200:
        raise RuntimeError(
            "Scan history request failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    history = response.json()

    if not isinstance(history, list):
        raise RuntimeError(
            f"Scan history response must be a list: {history}"
        )

    history_ids = [
        item.get("scan_id")
        for item in history
    ]

    if SCAN_ID not in history_ids:
        raise RuntimeError(
            "Persisted scan was not returned in authenticated scan history."
        )

    print("Scan history: PASS")
    print("Pagination: PASS")
    print("Persisted scan visible in history: PASS")


    # =======================================================================
    # TASK 113 — CROSS-USER ISOLATION
    # =======================================================================

    print()
    print("===== TASK 113 — CROSS-USER ISOLATION =====")

    response = client.get(
        f"/api/v1/ai/scans/{SCAN_ID}",
        headers=auth_headers(token_b),
    )

    if response.status_code != 404:
        raise RuntimeError(
            "Cross-user scan isolation FAILED.\n"
            f"Expected 404, received {response.status_code}\n"
            f"Body: {response.text}"
        )

    print("Cross-user single-scan isolation: PASS")

    response = client.get(
        "/api/v1/ai/scans",
        params={
            "limit": 100,
            "offset": 0,
        },
        headers=auth_headers(token_b),
    )

    if response.status_code != 200:
        raise RuntimeError(
            "User B scan history request failed.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    user_b_history = response.json()

    if any(
        item.get("scan_id") == SCAN_ID
        for item in user_b_history
    ):
        raise RuntimeError(
            "Cross-user scan history isolation FAILED."
        )

    print("Cross-user history isolation: PASS")


    # =======================================================================
    # TASK 114 — FINAL PERSISTENCE + CLEANUP GATE
    # =======================================================================

    print()
    print("===== TASK 114 — FINAL PERSISTENCE + CLEANUP GATE =====")

    db = SessionLocal()

    try:

        persisted_before_cleanup = db.execute(
            select(Scan).where(
                Scan.id == SCAN_ID,
                Scan.user_id == USER_A_ID,
            )
        ).scalar_one_or_none()

        if persisted_before_cleanup is None:
            raise RuntimeError(
                "Final persistence verification failed."
            )

        print("Final persisted scan verification: PASS")

        user_a = db.execute(
            select(User).where(
                User.email == USER_A_EMAIL,
            )
        ).scalar_one_or_none()

        user_b = db.execute(
            select(User).where(
                User.email == USER_B_EMAIL,
            )
        ).scalar_one_or_none()

        if user_a is None or user_b is None:
            raise RuntimeError(
                "Runtime test users could not be located for cleanup."
            )

        USER_A_ID = user_a.id
        USER_B_ID = user_b.id

        print("Temporary User A located: PASS")
        print("Temporary User B located: PASS")

        # Delete scan first because scans.user_id references users.id.
        db.query(Scan).filter(
            Scan.id == SCAN_ID
        ).delete(
            synchronize_session=False
        )

        db.query(User).filter(
            User.id.in_([
                USER_A_ID,
                USER_B_ID,
            ])
        ).delete(
            synchronize_session=False
        )

        db.commit()

        print("Temporary scan cleanup: PASS")
        print("Temporary user cleanup: PASS")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


    # =======================================================================
    # FINAL DATABASE CLEANLINESS CHECK
    # =======================================================================

    print()
    print("===== FINAL DATABASE CLEANLINESS CHECK =====")

    db = SessionLocal()

    try:

        remaining_scan = db.execute(
            select(Scan).where(
                Scan.id == SCAN_ID
            )
        ).scalar_one_or_none()

        remaining_user_a = db.execute(
            select(User).where(
                User.email == USER_A_EMAIL
            )
        ).scalar_one_or_none()

        remaining_user_b = db.execute(
            select(User).where(
                User.email == USER_B_EMAIL
            )
        ).scalar_one_or_none()

        if remaining_scan is not None:
            raise RuntimeError(
                "Temporary scan still exists after cleanup."
            )

        if remaining_user_a is not None:
            raise RuntimeError(
                "Temporary User A still exists after cleanup."
            )

        if remaining_user_b is not None:
            raise RuntimeError(
                "Temporary User B still exists after cleanup."
            )

        print("Temporary scan removed: PASS")
        print("Temporary User A removed: PASS")
        print("Temporary User B removed: PASS")
        print("Database cleanup: PASS")

    finally:
        db.close()


    print()
    print("=" * 80)
    print("TASKS 106-114 COMPLETE")
    print("=" * 80)

    print("Database connectivity: PASS")
    print("Authenticated User A: PASS")
    print("Authenticated User B: PASS")
    print("Real Gemini scanner request: PASS")
    print("Scanner response contract: PASS")
    print("Database persistence: PASS")
    print("Stable scan_id: PASS")
    print("Single scan retrieval: PASS")
    print("Scan history: PASS")
    print("Pagination: PASS")
    print("Cross-user isolation: PASS")
    print("Temporary data cleanup: PASS")
    print()
    print("SCANNER PERSISTENCE RUNTIME VALIDATION: PASS")
    print("=" * 80)

except Exception as exc:

    print()
    print("=" * 80)
    print("TASKS 106-114 FAILED")
    print("=" * 80)
    print(type(exc).__name__ + ":", str(exc))
    print()
    print(
        "IMPORTANT: Runtime test may have created temporary data "
        "before the failure."
    )
    print("Inspect database state before continuing.")
    print("=" * 80)

    raise
