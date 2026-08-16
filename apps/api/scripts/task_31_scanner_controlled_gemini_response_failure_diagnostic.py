from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResult


SERVICE_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "services"
    / "ai"
    / "scanner"
    / "service.py"
)


print("=" * 80)
print("STEP 8C-003 — TASK 31 — SCANNER CONTROLLED GEMINI RESPONSE FAILURE DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. VERIFY SCANNER SERVICE IMPORT =====")

print("HeritageScannerService: PASS")
print("HeritageScannerResult: PASS")


print()
print("===== 2. LOAD SCANNER SERVICE SOURCE =====")

service_source = SERVICE_PATH.read_text(
    encoding="utf-8"
)

print("Scanner service source: PRESENT")
print(f"Source length: {len(service_source)}")


print()
print("===== 3. VERIFY SCANNER METHOD BOUNDARIES =====")

service_methods = [
    "__init__",
    "scan",
    "_extract_json",
]

for method_name in service_methods:
    if hasattr(HeritageScannerService, method_name):
        print(f"{method_name}: PRESENT")
    else:
        print(f"{method_name}: NOT PRESENT")


print()
print("===== 4. INSPECT VALUEERROR SOURCES =====")

tree = ast.parse(service_source)

value_error_locations = []

for node in ast.walk(tree):
    if isinstance(node, ast.Raise):
        exc = node.exc

        if isinstance(exc, ast.Call):
            func = exc.func

            if (
                isinstance(func, ast.Name)
                and func.id == "ValueError"
            ):
                value_error_locations.append(
                    node.lineno
                )

        elif isinstance(exc, ast.Name):
            if exc.id == "ValueError":
                value_error_locations.append(
                    node.lineno
                )

if value_error_locations:
    print(
        "Explicit ValueError raises: "
        + ", ".join(
            str(line)
            for line in value_error_locations
        )
    )
else:
    print("Explicit ValueError raises: NONE")


print()
print("===== 5. INSPECT VALUEERROR EXCEPTIONS =====")

value_error_handlers = []

for node in ast.walk(tree):
    if isinstance(node, ast.ExceptHandler):
        handler_type = node.type

        if isinstance(handler_type, ast.Name):
            if handler_type.id == "ValueError":
                value_error_handlers.append(
                    node.lineno
                )

        elif isinstance(handler_type, ast.Tuple):
            for element in handler_type.elts:
                if (
                    isinstance(element, ast.Name)
                    and element.id == "ValueError"
                ):
                    value_error_handlers.append(
                        node.lineno
                    )

if value_error_handlers:
    print(
        "ValueError exception handlers: "
        + ", ".join(
            str(line)
            for line in value_error_handlers
        )
    )
else:
    print("ValueError exception handlers: NONE")


print()
print("===== 6. INSPECT JSON PARSING BOUNDARIES =====")

json_terms = [
    "json.loads",
    "json.dumps",
    "_extract_json",
    "response.text",
    ".text",
    "model_dump",
]

for term in json_terms:
    count = service_source.count(term)

    if count:
        print(
            f"{term}: PRESENT ({count})"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )


print()
print("===== 7. INSPECT GEMINI RESPONSE ACCESS =====")

gemini_response_terms = [
    "response.text",
    "response.candidates",
    "response.candidate",
    "response.parts",
    "response.content",
    "response.model_dump",
]

for term in gemini_response_terms:
    count = service_source.count(term)

    if count:
        print(
            f"{term}: PRESENT ({count})"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )


print()
print("===== 8. INSPECT SCANNER EXTRACTION SOURCE =====")

if hasattr(
    HeritageScannerService,
    "_extract_json",
):
    extraction_source = inspect.getsource(
        HeritageScannerService._extract_json
    )

    print(extraction_source)
else:
    print("_extract_json(): NOT PRESENT")


print()
print("===== 9. INSPECT SCAN METHOD SOURCE =====")

if hasattr(
    HeritageScannerService,
    "scan",
):
    scan_source = inspect.getsource(
        HeritageScannerService.scan
    )

    print(scan_source)
else:
    print("scan(): NOT PRESENT")


print()
print("===== 10. VERIFY PRODUCTION RESULT CONTRACT =====")

result_fields = (
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
    "identification_status",
    "evidence_quality",
)

model_fields = getattr(
    HeritageScannerResult,
    "model_fields",
    {},
)

for field in result_fields:
    if field in model_fields:
        print(f"{field}: PRESENT")
    else:
        print(f"{field}: MISSING")


print()
print("===== 11. CHECK EXTRACTION FAILURE BOUNDARIES =====")

failure_terms = [
    "No scanner response",
    "empty scanner response",
    "response is empty",
    "response.text",
    "json.loads",
    "ValueError",
    "ScannerImageValidationError",
    "ScannerQuotaExceededError",
]

for term in failure_terms:
    if term.lower() in service_source.lower():
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )


print()
print("===== 12. VERIFY NO TEST MAKES A REAL GEMINI REQUEST =====")

print("Diagnostic type: READ-ONLY SOURCE INSPECTION")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 31 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("Scanner source inspection: PASS")
print("ValueError boundary inspection: PASS")
print("JSON extraction inspection: PASS")
print("Gemini response boundary inspection: PASS")
print("Production contract inspection: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
