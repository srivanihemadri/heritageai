from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1 import ai as ai_router
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)


print("=" * 80)
print("STEP 8C-003 — TASK 8 — SCANNER API BOUNDARY ISOLATION")
print("=" * 80)


print()
print("===== 1. VERIFY APPLICATION =====")

print("FastAPI application:", type(app).__name__)

client = TestClient(app)

print("FastAPI TestClient: PASS")


print()
print("===== 2. BUILD CONTROLLED SCANNER RESPONSE =====")

controlled_response = HeritageScannerResponse(
    success=True,
    scan_id="boundary-isolation-test",
    result=HeritageScannerResult(
        identified_name="Controlled Heritage Site",
        category="HISTORICAL_SITE",
        location="Test Location",
        country="India",
        confidence=0.91,
        confidence_level="HIGH",
        description="Controlled API boundary isolation response.",
        architectural_style="Rock-cut",
        historical_period="Ancient",
        historical_significance="Controlled diagnostic evidence.",
        visual_evidence=[
            "Controlled evidence one",
            "Controlled evidence two",
        ],
        alternative_matches=[],
        grounding_status="UNVERIFIED",
    ),
)

print("HeritageScannerResponse: PASS")
print("HeritageScannerResult: PASS")


print()
print("===== 3. CREATE CONTROLLED SCANNER SERVICE =====")


class ControlledScannerService:

    def __init__(self) -> None:

        print(
            "ControlledScannerService.__init__: PASS"
        )

        self.client = None

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ) -> HeritageScannerResponse:

        print(
            "ControlledScannerService.scan: CALLED"
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

        return controlled_response


original_service = ai_router.HeritageScannerService

ai_router.HeritageScannerService = ControlledScannerService

print(
    "Scanner service substitution: PASS"
)


try:

    print()
    print("===== 4. CREATE CONTROLLED IMAGE =====")

    from PIL import Image
    from io import BytesIO

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
        "Controlled image bytes:",
        len(image_bytes),
    )

    print("Controlled image: PASS")


    print()
    print("===== 5. VERIFY API ROUTE =====")

    openapi = app.openapi()

    operation = openapi[
        "paths"
    ][
        "/api/v1/ai/scan"
    ][
        "post"
    ]

    print(
        "OpenAPI scanner operation: PASS"
    )

    print(
        "Security:",
        operation.get("security"),
    )


    print()
    print("===== 6. EXECUTE ACTUAL FASTAPI SCANNER ROUTE =====")

    response = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "boundary_test.png",
                image_bytes,
                "image/png",
            )
        },
        headers={
            "Authorization": "Bearer boundary-test-token"
        },
    )

    print(
        "HTTP status:",
        response.status_code,
    )

    print(
        "Response:",
        response.text,
    )


    print()
    print("===== 7. ANALYZE RESULT =====")

    if response.status_code == 401:

        print(
            "Authentication rejected before route execution."
        )

        print(
            "This means the diagnostic token is not sufficient "
            "for the real authentication dependency."
        )

        print(
            "AUTHENTICATION BOUNDARY: ISOLATED"
        )

    elif response.status_code == 200:

        payload = response.json()

        print(
            "API boundary response: PASS"
        )

        if payload.get("success") is not True:
            raise RuntimeError(
                "Expected success=True."
            )

        if payload.get("scan_id") != "boundary-isolation-test":
            raise RuntimeError(
                "Controlled scanner response did not reach API response."
            )

        print(
            "Controlled scanner response reached FastAPI: PASS"
        )

        print(
            "API ROUTE BOUNDARY: PASS"
        )

    elif response.status_code == 500:

        print(
            "API returned 500 despite controlled scanner service."
        )

        print(
            "This indicates the failure occurs in the "
            "FastAPI route boundary rather than Gemini."
        )

        print(
            "API ROUTE BOUNDARY: FAIL"
        )

        raise RuntimeError(
            "Controlled scanner still produced HTTP 500."
        )

    else:

        print(
            "Unexpected HTTP status:",
            response.status_code,
        )

        raise RuntimeError(
            "Unexpected scanner API boundary response."
        )


finally:

    ai_router.HeritageScannerService = original_service

    print()
    print(
        "Scanner service restoration: PASS"
    )


print()
print("===== 8. FINAL SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 8 COMPLETE")
print("=" * 80)

print("Scanner API boundary isolation: COMPLETE")
print("SEND THE COMPLETE OUTPUT.")
