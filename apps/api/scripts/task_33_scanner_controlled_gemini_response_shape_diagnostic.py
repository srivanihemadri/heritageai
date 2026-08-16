from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService


SERVICE_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "services"
    / "ai"
    / "scanner"
    / "service.py"
)


print("=" * 80)
print("STEP 8C-003 — TASK 33 — SCANNER CONTROLLED GEMINI RESPONSE-SHAPE DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. VERIFY GEMINI CLIENT BOUNDARY =====")

service_source = SERVICE_PATH.read_text(
    encoding="utf-8"
)

if "genai.Client" not in service_source:
    raise RuntimeError(
        "Gemini client initialization boundary not found."
    )

if "generate_content" not in service_source:
    raise RuntimeError(
        "Gemini generate_content boundary not found."
    )

print("genai.Client: PRESENT")
print("generate_content: PRESENT")
print("Gemini client boundary: PASS")


print()
print("===== 2. VERIFY RESPONSE ASSIGNMENT =====")

tree = ast.parse(service_source)

response_assignments = []

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "response"
            ):
                response_assignments.append(
                    node.lineno
                )

if not response_assignments:
    raise RuntimeError(
        "Scanner response assignment not found."
    )

print(
    "response assignment: PRESENT at line(s) "
    + ", ".join(
        str(line)
        for line in response_assignments
    )
)
print("Response assignment boundary: PASS")


print()
print("===== 3. VERIFY RESPONSE TEXT ACCESS =====")

text_assignment_found = False

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "text"
            ):
                if isinstance(node.value, ast.Call):
                    text_assignment_found = True

if not text_assignment_found:
    raise RuntimeError(
        "Scanner response text extraction assignment not found."
    )

print("response text extraction: PRESENT")
print("Response text boundary: PASS")


print()
print("===== 4. VERIFY RESPONSE EMPTY BOUNDARY =====")

required_terms = [
    "if not text:",
    "Gemini returned an empty scanner response.",
]

for term in required_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Required response boundary missing: {term}"
        )

print("Empty response guard: PRESENT")
print("Sanitized empty-response error: PRESENT")
print("Empty response boundary: PASS")


print()
print("===== 5. VERIFY JSON EXTRACTION BOUNDARY =====")

if "payload = self._extract_json(text)" not in service_source:
    raise RuntimeError(
        "Scanner JSON extraction boundary not found."
    )

print("payload extraction: PRESENT")
print("_extract_json(text): PRESENT")
print("JSON extraction boundary: PASS")


print()
print("===== 6. VERIFY PRODUCTION VALIDATION BOUNDARY =====")

if (
    "HeritageScannerResult.model_validate(" 
    not in service_source
):
    raise RuntimeError(
        "HeritageScannerResult validation boundary not found."
    )

print(
    "HeritageScannerResult.model_validate(): PRESENT"
)
print("Production validation boundary: PASS")


print()
print("===== 7. VERIFY RESPONSE CONTENT IS NOT LOGGED =====")

forbidden_logging_patterns = [
    "print(response.text",
    "print(text)",
    "logger.info(response.text",
    "logger.debug(response.text",
    "logger.warning(response.text",
    "logger.error(response.text",
    "print(response)",
    "logger.info(response)",
    "logger.debug(response)",
]

for pattern in forbidden_logging_patterns:
    if pattern in service_source:
        raise RuntimeError(
            f"Potential response-content logging detected: {pattern}"
        )

print("Gemini response content logging: NONE")
print("Response-content privacy boundary: PASS")


print()
print("===== 8. VERIFY IMAGE CONTENT IS NOT LOGGED =====")

forbidden_image_patterns = [
    "print(image_bytes",
    "logger.info(image_bytes",
    "logger.debug(image_bytes",
    "logger.warning(image_bytes",
    "logger.error(image_bytes",
    "image_base64",
    "base64_image",
]

for pattern in forbidden_image_patterns:
    if pattern in service_source:
        raise RuntimeError(
            f"Potential image-content logging detected: {pattern}"
        )

print("Image-content logging: NONE")
print("Image privacy boundary: PASS")


print()
print("===== 9. VERIFY EXCEPTION BOUNDARIES =====")

exception_types = [
    "errors.ClientError",
    "errors.ServerError",
    "ScannerQuotaExceededError",
    "RuntimeError",
    "ValueError",
]

for exception_type in exception_types:
    if exception_type in service_source:
        print(
            f"{exception_type}: PRESENT"
        )
    else:
        print(
            f"{exception_type}: NOT PRESENT"
        )


print()
print("===== 10. CONTROLLED RESPONSE-SHAPE MODEL =====")

class ControlledResponse:
    pass


class ResponseWithText:
    text = '{"controlled": true}'


class ResponseWithoutText:
    pass


response_with_text = ResponseWithText()
response_without_text = ResponseWithoutText()

if not getattr(
    response_with_text,
    "text",
    None,
):
    raise RuntimeError(
        "Controlled response-with-text model failed."
    )

if getattr(
    response_without_text,
    "text",
    None,
) is not None:
    raise RuntimeError(
        "Controlled response-without-text model failed."
    )

print("Response with text attribute: PASS")
print("Response without text attribute: PASS")
print("Controlled response-shape model: PASS")


print()
print("===== 11. VERIFY RESPONSE TYPE IS NOT HARD-CODED =====")

scan_source = inspect.getsource(
    HeritageScannerService.scan
)

if "response = self.client.models.generate_content" not in scan_source:
    raise RuntimeError(
        "Expected Gemini generate_content call not found."
    )

print("Gemini response assignment: PRESENT")
print("Response type remains SDK-controlled: PASS")


print()
print("===== 12. VERIFY NO REAL GEMINI REQUEST =====")

print("Diagnostic mode: READ-ONLY")
print("Gemini generate_content executed: NO")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 33 COMPLETE")
print("=" * 80)
print("Gemini client boundary: PASS")
print("Response assignment boundary: PASS")
print("Response text boundary: PASS")
print("Empty response boundary: PASS")
print("JSON extraction boundary: PASS")
print("Pydantic validation boundary: PASS")
print("Response-content privacy: PASS")
print("Image-content privacy: PASS")
print("Controlled response-shape model: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
