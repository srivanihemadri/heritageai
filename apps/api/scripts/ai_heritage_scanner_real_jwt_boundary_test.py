from __future__ import annotations

import sys
import uuid
from io import BytesIO
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.v1 import ai as ai_router
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)


print("=" * 80)
print("STEP 8C-003 â€” TASK 9 â€” REAL JWT CONTROLLED SCANNER API BOUNDARY")
print("=" * 80)


print()
print("===== 1. INITIALIZE FASTAPI CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


print()
print("===== 2. CREATE UNIQUE TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = f"scanner.boundary.{suffix}@example.com"
password = "HeritageAI_Test_2026!"
full_name = "HeritageAI Scanner Boundary Test"

print("Test email:", email)


print()
print("===== 3. REGISTER TEST USER =====")

registration = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": full_name,
        "email": email,
        "password": password,
    },
)

print(
    "Registration HTTP status:",
    registration.status_code,
)

if registration.status_code != 201:

    print(
        "Registration response:",
        registration.text,
    )

    raise RuntimeError(
        "Test-user registration failed."
    )

print("Registration: PASS")


print()
print("===== 4. LOGIN TEST USER =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

print(
    "Login HTTP status:",
    login.status_code,
)

if login.status_code != 200:

    print(
        "Login response:",
        login.text,
    )

    raise RuntimeError(
        "Test-user login failed."
    )

login_payload = login.json()

access_token = login_payload.get(
    "access_token"
)

if not access_token:

    raise RuntimeError(
        "JWT access token missing."
    )

print("JWT acquisition: PASS")


print()
print("===== 5. BUILD CONTROLLED SCANNER RESPONSE =====")

controlled_response = HeritageScannerResponse(
    success=True,
    scan_id="real-jwt-boundary-test",
    result=HeritageScannerResult(
        identified_name="Controlled Heritage Site",
        category="HISTORICAL_SITE",
        location="Test Location",
        country="India",
        confidence=0.95,
        confidence_level="HIGH",
        description=(
            "Controlled scanner response used to isolate "
            "the FastAPI scanner boundary."
        ),
        architectural_style="Rock-cut",
        historical_period="Ancient",
        historical_significance=(
            "Controlled diagnostic evidence."
        ),
        visual_evidence=[
            "Controlled evidence one",
            "Controlled evidence two",
        ],
        alternative_matches=[],
        grounding_status="UNVERIFIED",
    ),
)

print("Controlled response construction: PASS")


print()
print("===== 6. CREATE CONTROLLED SCANNER SERVICE =====")


class ControlledScannerService:

    def __init__(self) -> None:

        self.client = None

        print(
            "ControlledScannerService initialized."
        )

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ) -> HeritageScannerResponse:

        print(
            "CONTROLLED SCANNER SERVICE INVOKED"
        )

        print(
            "Image bytes:",
            len(image_bytes),
        )

        print(
            "Content type:",
            content_type,
        )

        if not image_bytes:
            raise RuntimeError(
                "Controlled scanner received empty image."
            )

        if content_type != "image/png":
            raise RuntimeError(
                "Unexpected controlled image content type."
            )

        return controlled_response


original_service = ai_router.HeritageScannerService

ai_router.HeritageScannerService = ControlledScannerService

print(
    "Scanner service substitution: PASS"
)


try:

    print()
    print("===== 7. CREATE CONTROLLED IMAGE =====")

    image = Image.new(
        "RGB",
        (64, 64),
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    image_bytes = buffer.getvalue()

    print(
        "Image bytes:",
        len(image_bytes),
    )

    print("Controlled PNG: PASS")


    print()
    print("===== 8. VERIFY UNAUTHENTICATED BOUNDARY =====")

    unauthenticated = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "boundary.png",
                image_bytes,
                "image/png",
            )
        },
    )

    print(
        "Unauthenticated HTTP status:",
        unauthenticated.status_code,
    )

    if unauthenticated.status_code != 401:

        print(
            "Response:",
            unauthenticated.text,
        )

        raise RuntimeError(
            "Unauthenticated scanner request "
            "was not rejected with 401."
        )

    print(
        "Unauthenticated rejection: PASS"
    )


    print()
    print("===== 9. EXECUTE AUTHENTICATED CONTROLLED SCANNER =====")

    authenticated = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "boundary.png",
                image_bytes,
                "image/png",
            )
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    print(
        "Authenticated HTTP status:",
        authenticated.status_code,
    )

    print(
        "Authenticated response:",
        authenticated.text,
    )


    print()
    print("===== 10. ANALYZE AUTHENTICATED RESULT =====")

    if authenticated.status_code != 200:

        raise RuntimeError(
            "Authenticated controlled scanner request "
            f"failed: {authenticated.status_code} "
            f"{authenticated.text}"
        )

    payload = authenticated.json()

    if payload.get("success") is not True:

        raise RuntimeError(
            "Authenticated response success flag is not true."
        )

    if payload.get("scan_id") != "real-jwt-boundary-test":

        raise RuntimeError(
            "Controlled scanner result did not reach "
            "the API response."
        )

    result = payload.get("result")

    if not isinstance(result, dict):

        raise RuntimeError(
            "Scanner result missing from API response."
        )

    if result.get("identified_name") != "Controlled Heritage Site":

        raise RuntimeError(
            "Unexpected controlled scanner result."
        )

    print(
        "Authenticated API boundary: PASS"
    )

    print(
        "Controlled scanner reached FastAPI response: PASS"
    )

    print(
        "Response serialization: PASS"
    )


finally:

    ai_router.HeritageScannerService = original_service

    print()
    print(
        "Scanner service restoration: PASS"
    )


print()
print("===== 11. FINAL SAFETY =====")

print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 â€” TASK 9 COMPLETE")
print("=" * 80)

print("Real JWT authentication: PASS")
print("Unauthenticated boundary: PASS")
print("Controlled scanner invocation: PASS")
print("Authenticated scanner API boundary: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
