from __future__ import annotations

import inspect
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

print("=" * 80)
print("STEP 8C-003 — TASK 6 — SCANNER API INTEGRATION ROOT-CAUSE AUDIT")
print("=" * 80)

print()
print("===== 1. IMPORT AI ROUTER =====")

from app.api.v1.ai import router

print("AI router import: PASS")
print("Router prefix:", router.prefix)

print()
print("===== 2. FIND SCANNER ROUTE =====")

scanner_routes = [
    route
    for route in router.routes
    if getattr(route, "path", None) == "/ai/scan"
    and "POST" in getattr(route, "methods", set())
]

if len(scanner_routes) != 1:
    print("Expected exactly one POST /ai/scan route.")
    print("Found:", len(scanner_routes))

    for route in router.routes:
        print(
            "ROUTE:",
            getattr(route, "path", None),
            getattr(route, "methods", None),
        )

    raise RuntimeError("Scanner route uniqueness validation failed.")

route = scanner_routes[0]

print("POST /ai/scan: PASS")

print()
print("===== 3. INSPECT ROUTE ENDPOINT =====")

endpoint = route.endpoint

print("Endpoint:", endpoint)
print("Endpoint name:", getattr(endpoint, "__name__", "<unknown>"))

print()
print("===== 4. INSPECT ROUTE SIGNATURE =====")

signature = inspect.signature(endpoint)

print("Signature:", signature)

for name, parameter in signature.parameters.items():
    print()
    print("PARAMETER:", name)
    print("  annotation:", parameter.annotation)
    print("  default:", parameter.default)

print()
print("===== 5. VERIFY UPLOADFILE PARAMETER =====")

upload_parameters = []

for name, parameter in signature.parameters.items():

    annotation = parameter.annotation

    if (
        "UploadFile" in str(annotation)
        or "UploadFile" in repr(annotation)
    ):
        upload_parameters.append(name)

if not upload_parameters:
    raise RuntimeError(
        "No UploadFile parameter detected in scanner endpoint."
    )

print("UploadFile parameters:", upload_parameters)
print("UploadFile contract: PASS")

print()
print("===== 6. VERIFY AUTHENTICATION DEPENDENCY =====")

dependencies = []

for dependency in route.dependant.dependencies:
    call = dependency.call

    if call is not None:
        dependencies.append(getattr(call, "__name__", str(call)))

print("Route dependencies:", dependencies)

if "get_current_user" not in dependencies:
    raise RuntimeError(
        "Scanner endpoint missing get_current_user dependency."
    )

print("Authentication dependency: PASS")

print()
print("===== 7. IMPORT SCANNER SERVICE =====")

from app.services.ai.scanner.service import HeritageScannerService

print("HeritageScannerService: PASS")

service_signature = inspect.signature(
    HeritageScannerService.scan
)

print("Service scan signature:", service_signature)

print()
print("===== 8. VERIFY SERVICE CONTRACT =====")

expected_parameters = {
    "image_bytes",
    "content_type",
}

actual_parameters = set(
    service_signature.parameters.keys()
)

print("Expected parameters:", expected_parameters)
print("Actual parameters:", actual_parameters)

missing = expected_parameters - actual_parameters

if missing:
    raise RuntimeError(
        f"Scanner service contract missing parameters: {missing}"
    )

print("Scanner service contract: PASS")

print()
print("===== 9. INSPECT SCANNER ROUTE SOURCE =====")

try:
    source = inspect.getsource(endpoint)

    print(source)

except Exception as exc:
    print(
        "Could not retrieve endpoint source:",
        repr(exc),
    )

print()
print("===== 10. VERIFY EXPECTED SERVICE INVOCATION PATTERN =====")

try:
    source = inspect.getsource(endpoint)
except Exception:
    source = ""

patterns = [
    "HeritageScannerService",
    ".read()",
    "content_type",
    "image_bytes",
]

for pattern in patterns:

    if pattern not in source:
        print(
            f"WARNING: expected pattern not detected: {pattern}"
        )
    else:
        print(f"{pattern}: PASS")

print()
print("===== 11. VERIFY ROUTE RESPONSE MODEL =====")

print(
    "Response model:",
    getattr(route, "response_model", None),
)

if getattr(route, "response_model", None) is None:
    raise RuntimeError(
        "Scanner route has no response model."
    )

print("Response model: PASS")

print()
print("===== 12. VERIFY FASTAPI APPLICATION ROUTE =====")

from app.main import app

application_matches = [
    route
    for route in app.routes
    if getattr(route, "path", None) == "/api/v1/ai/scan"
    and "POST" in getattr(route, "methods", set())
]

print(
    "Application POST /api/v1/ai/scan matches:",
    len(application_matches),
)

if len(application_matches) != 1:
    raise RuntimeError(
        "Expected exactly one application scanner route."
    )

print("Application scanner route: PASS")

print()
print("===== 13. VERIFY OPENAPI =====")

openapi = app.openapi()

operation = openapi["paths"].get(
    "/api/v1/ai/scan"
)

if operation is None:
    raise RuntimeError(
        "OpenAPI scanner endpoint missing."
    )

print("OpenAPI scanner endpoint: PASS")
print("OpenAPI methods:", list(operation.keys()))

if "post" not in operation:
    raise RuntimeError(
        "OpenAPI POST scanner operation missing."
    )

print("POST operation: PASS")

print()
print("===== 14. VERIFY MULTIPART REQUEST BODY =====")

request_body = operation["post"].get("requestBody")

print("Request body:", request_body)

if request_body is None:
    raise RuntimeError(
        "Scanner endpoint has no OpenAPI request body."
    )

content = request_body.get("content", {})

if "multipart/form-data" not in content:
    raise RuntimeError(
        "Scanner endpoint is not declared as multipart/form-data."
    )

print("multipart/form-data: PASS")

print()
print("===== 15. DATABASE SAFETY =====")

print(
    "No database connection created by this audit."
)

print("Database mutation: NONE")
print("Gemini request: NONE")
print("Qdrant mutation: NONE")
print("Embedding creation: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 6 COMPLETE")
print("=" * 80)

print("Scanner route architecture: PASS")
print("UploadFile contract: PASS")
print("Authentication boundary: PASS")
print("Scanner service contract: PASS")
print("Application route: PASS")
print("OpenAPI multipart contract: PASS")
print("NO PRODUCTION SOURCE CHANGES MADE.")
print("DO NOT RUN GEMINI.")
print("SEND THE COMPLETE OUTPUT.")
