from __future__ import annotations

import inspect
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.api.v1.ai import heritage_scan
from app.services.ai.scanner.contract import HeritageScannerResponse


print("=" * 80)
print("STEP 8C-003 — TASK 7 — SCANNER API 500 ROOT-CAUSE CAPTURE")
print("=" * 80)

print()
print("===== 1. IMPORT ENDPOINT =====")

print("Endpoint:", heritage_scan)
print("Endpoint name:", heritage_scan.__name__)

print("Endpoint import: PASS")


print()
print("===== 2. READ ENDPOINT SOURCE =====")

source = inspect.getsource(heritage_scan)

print(source)

print()
print("Endpoint source inspection: PASS")


print()
print("===== 3. VERIFY EXCEPTION BOUNDARY =====")

required_patterns = [
    "ScannerImageValidationError",
    "HTTPException",
    "SCANNER_FAILURE",
    "HeritageScannerService",
    "service.scan",
    "await file.read()",
]

for pattern in required_patterns:

    if pattern not in source:
        raise RuntimeError(
            f"Required endpoint pattern missing: {pattern}"
        )

    print(f"{pattern}: PASS")


print()
print("===== 4. VERIFY RESPONSE CONTRACT =====")

from app.services.ai.scanner.contract import HeritageScannerResult

test_result = HeritageScannerResponse(
    scan_id="diagnostic-scan",
    result=HeritageScannerResult(
        identified_name=None,
        category=None,
        location=None,
        country=None,
        confidence=0.0,
        confidence_level="LOW",
        description="Diagnostic response.",
        architectural_style=None,
        historical_period=None,
        historical_significance=None,
        visual_evidence=["Diagnostic evidence."],
        alternative_matches=[],
        grounding_status="UNVERIFIED",
    ),
)

print("HeritageScannerResponse construction: PASS")

try:
    dumped = test_result.model_dump()

    print("model_dump: PASS")
    print("Dump:", dumped)

except Exception as exc:

    print(
        "Response serialization failure:",
        type(exc).__name__,
        str(exc),
    )

    raise


print()
print("===== 5. VERIFY RESPONSE JSON SERIALIZATION =====")

try:

    json_payload = test_result.model_dump_json()

    print("model_dump_json: PASS")
    print("JSON length:", len(json_payload))

except Exception as exc:

    print(
        "JSON serialization failure:",
        type(exc).__name__,
        str(exc),
    )

    raise


print()
print("===== 6. INSPECT SERVICE CLEANUP =====")

from app.services.ai.scanner.service import HeritageScannerService

service_source = inspect.getsource(
    HeritageScannerService
)

print(service_source)

print("Scanner service source inspection: PASS")


print()
print("===== 7. INSPECT SERVICE CLOSE =====")

close_method = getattr(
    HeritageScannerService,
    "close",
    None,
)

if close_method is None:

    print(
        "HeritageScannerService.close(): NOT DEFINED"
    )

else:

    print(
        "HeritageScannerService.close(): PRESENT"
    )

    print(
        inspect.signature(close_method)
    )

print()
print("===== 8. VERIFY CLIENT CLEANUP BEHAVIOR =====")

try:

    service = HeritageScannerService()

    client = getattr(
        service,
        "client",
        None,
    )

    print(
        "Client type:",
        type(client).__name__
        if client is not None
        else None,
    )

    close = getattr(
        client,
        "close",
        None,
    )

    print(
        "Client close callable:",
        callable(close),
    )

    if callable(close):

        print(
            "IMPORTANT: Diagnostic will NOT call client.close()."
        )

    print("Client cleanup inspection: PASS")

except Exception as exc:

    print(
        "Service initialization failure:",
        type(exc).__name__,
        str(exc),
    )

    raise


print()
print("===== 9. VERIFY FASTAPI RESPONSE MODEL =====")

from app.main import app

openapi = app.openapi()

operation = openapi["paths"]["/api/v1/ai/scan"]["post"]

response_schema = (
    operation["responses"]["200"]
    ["content"]["application/json"]
    ["schema"]
)

print(
    "Response schema:",
    response_schema,
)

print("FastAPI response schema: PASS")


print()
print("===== 10. FINAL DIAGNOSTIC RESULT =====")

print("Endpoint source: PASS")
print("Exception boundary: PASS")
print("Scanner response contract: PASS")
print("JSON serialization: PASS")
print("Service cleanup inspection: PASS")
print("OpenAPI response contract: PASS")

print()
print("NO GEMINI REQUEST MADE.")
print("NO DATABASE QUERIES MADE.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 7 COMPLETE")
print("=" * 80)

print("SEND THE COMPLETE OUTPUT.")
