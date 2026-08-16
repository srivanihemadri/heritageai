from __future__ import annotations

import inspect
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.api.v1 import ai as ai_router
from app.services.ai.scanner import image as scanner_image
from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 12A — SCANNER BINARY IMAGE VALIDATION AUDIT")
print("=" * 80)


print()
print("===== 1. SCANNER IMAGE MODULE =====")

print(
    "Module:",
    scanner_image.__file__,
)

print(
    "ScannerImageValidationError:",
    getattr(
        scanner_image,
        "ScannerImageValidationError",
        None,
    ),
)

print("Image module import: PASS")


print()
print("===== 2. IMAGE MODULE SYMBOLS =====")

symbols = [
    name
    for name in dir(scanner_image)
    if not name.startswith("_")
]

for name in symbols:
    print(
        "SYMBOL:",
        name,
    )


print()
print("===== 3. IMAGE MODULE SOURCE =====")

image_source = inspect.getsource(
    scanner_image
)

print(image_source)


print()
print("===== 4. SCANNER SERVICE SOURCE =====")

service_source = inspect.getsource(
    HeritageScannerService
)

print(service_source)


print()
print("===== 5. AI ROUTER SOURCE =====")

router_source = inspect.getsource(
    ai_router.heritage_scan
)

print(router_source)


print()
print("===== 6. VALIDATION REFERENCE ANALYSIS =====")

service_has_image_validation = (
    "ScannerImageValidationError"
    in service_source
)

service_has_image_open = (
    "Image.open"
    in service_source
)

service_has_validate = (
    "validate"
    in service_source.lower()
)

route_has_image_validation = (
    "ScannerImageValidationError"
    in router_source
)

route_has_validation_call = (
    "validate"
    in router_source.lower()
)

print(
    "Service references ScannerImageValidationError:",
    service_has_image_validation,
)

print(
    "Service references Image.open:",
    service_has_image_open,
)

print(
    "Service contains validation reference:",
    service_has_validate,
)

print(
    "Route references ScannerImageValidationError:",
    route_has_image_validation,
)

print(
    "Route contains validation call:",
    route_has_validation_call,
)


print()
print("===== 7. ROUTE PARAMETERS =====")

route = None

for candidate in ai_router.router.routes:

    if getattr(
        candidate,
        "path",
        None,
    ) == "/ai/scan":

        route = candidate
        break

if route is None:
    raise RuntimeError(
        "POST /ai/scan route not found."
    )

print(
    "Route:",
    route.path,
)

print(
    "Methods:",
    sorted(route.methods),
)

print(
    "Endpoint:",
    route.endpoint,
)

print(
    "Route dependencies:",
    [
        getattr(
            dependency.call,
            "__name__",
            str(dependency.call),
        )
        for dependency in route.dependant.dependencies
    ],
)


print()
print("===== 8. OPENAPI CONTRACT =====")

from app.main import app

openapi = app.openapi()

operation = (
    openapi
    .get("paths", {})
    .get("/api/v1/ai/scan", {})
    .get("post")
)

if operation is None:
    raise RuntimeError(
        "OpenAPI scanner operation missing."
    )

print(
    "Multipart request body:",
    "requestBody" in operation,
)

print(
    "Security:",
    operation.get("security"),
)


print()
print("===== 9. CURRENT VALIDATION ARCHITECTURE =====")

if service_has_image_open:
    print(
        "Binary image decoding appears in scanner service."
    )
else:
    print(
        "Binary image decoding NOT found in scanner service."
    )

if route_has_validation_call:
    print(
        "Route contains an explicit validation call."
    )
else:
    print(
        "Route does NOT contain an explicit validation call."
    )


print()
print("===== 10. DATABASE SAFETY =====")

print(
    "No database connection created."
)

print(
    "No database queries executed."
)

print(
    "No database mutations."
)


print()
print("===== 11. GEMINI SAFETY =====")

print(
    "No Gemini request executed."
)

print(
    "No embeddings created."
)

print(
    "No Qdrant changes."
)


print()
print("===== 12. PRODUCTION SAFETY =====")

print(
    "READ-ONLY AUDIT"
)

print(
    "NO PRODUCTION SOURCE CHANGES"
)


print()
print("=" * 80)
print("STEP 8C-003 — TASK 12A AUDIT COMPLETE")
print("=" * 80)

print(
    "SEND THE COMPLETE OUTPUT."
)
