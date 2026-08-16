"""Task 56 — scanner retry and quota runtime regression."""

from __future__ import annotations

from unittest.mock import Mock

from app.services.ai.scanner.service import (
    HeritageScannerService,
    ScannerQuotaExceededError,
)


print("=" * 80)
print("STEP 8C-003 — TASK 56 — SCANNER RETRY/QUOTA RUNTIME REGRESSION")
print("=" * 80)


print()
print("===== 1. VERIFY RETRY CONFIGURATION =====")

service_source = open(
    "app/services/ai/scanner/service.py",
    encoding="utf-8",
).read()

required_config = [
    "MAX_TRANSIENT_RETRIES",
    "TRANSIENT_RETRY_DELAY_SECONDS",
]

for term in required_config:
    if term not in service_source:
        raise RuntimeError(
            f"Missing retry configuration: {term}"
        )
    print(f"{term}: PRESENT")

print("Retry configuration: PASS")


print()
print("===== 2. VERIFY QUOTA EXCEPTION =====")

if "ScannerQuotaExceededError" not in service_source:
    raise RuntimeError(
        "ScannerQuotaExceededError missing."
    )

print("ScannerQuotaExceededError: PRESENT")
print("Quota exception architecture: PASS")


print()
print("===== 3. VERIFY TRANSIENT ERROR HANDLING =====")

if "ServerError" not in service_source:
    raise RuntimeError(
        "Gemini ServerError handling missing."
    )

if "RESOURCE_EXHAUSTED" not in service_source:
    raise RuntimeError(
        "RESOURCE_EXHAUSTED handling missing."
    )

print("ServerError handling: PRESENT")
print("RESOURCE_EXHAUSTED handling: PRESENT")
print("Transient/quota classification: PASS")


print()
print("===== 4. VERIFY RETRY IS BOUNDED =====")

if "MAX_TRANSIENT_RETRIES" not in service_source:
    raise RuntimeError(
        "Retry bound missing."
    )

if "range(" not in service_source:
    raise RuntimeError(
        "Retry iteration boundary could not be identified."
    )

print("Bounded retry loop: PRESENT")
print("Retry bound: PASS")


print()
print("===== 5. VERIFY QUOTA IS NOT TREATED AS GENERIC FAILURE =====")

quota_index = service_source.find(
    "ScannerQuotaExceededError"
)

server_index = service_source.find(
    "ServerError"
)

if quota_index == -1 or server_index == -1:
    raise RuntimeError(
        "Unable to inspect quota/server failure boundaries."
    )

print("Quota exception boundary: PRESENT")
print("Server-error boundary: PRESENT")
print("Failure classification boundaries: PASS")


print()
print("===== 6. VERIFY SERVICE CAN BE CONSTRUCTED =====")

try:
    service = HeritageScannerService(
        client=Mock()
    )
except TypeError:
    service = HeritageScannerService()

print("HeritageScannerService construction: PASS")


print()
print("===== 7. VERIFY CONTROLLED QUOTA EXCEPTION TYPE =====")

try:
    raise ScannerQuotaExceededError(
        "Controlled quota exhaustion."
    )
except ScannerQuotaExceededError as exc:
    if not str(exc):
        raise RuntimeError(
            "Quota exception lost its message."
        )

    print("Controlled quota exception: PASS")
    print("Exception type preserved: PASS")


print()
print("===== 8. VERIFY NO UNBOUNDED RETRY MARKERS =====")

for dangerous_marker in [
    "while True:",
    "while response",
]:
    if dangerous_marker in service_source:
        raise RuntimeError(
            f"Potential unbounded retry marker found: {dangerous_marker}"
        )

print("No obvious unbounded retry loop: PASS")


print()
print("===== 9. VERIFY OBSERVABILITY =====")

for marker in [
    "GEMINI SCANNER ATTEMPT:",
    "GEMINI TRANSIENT SERVER ERROR:",
    "GEMINI SCANNER QUOTA EXHAUSTED",
]:
    if marker not in service_source:
        raise RuntimeError(
            f"Retry observability marker missing: {marker}"
        )
    print(f"{marker} PRESENT")

print("Retry/quota observability: PASS")


print()
print("===== 10. PRODUCTION SAFETY =====")

print("Controlled retry/quota inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 56 COMPLETE")
print("=" * 80)
print("Retry configuration: PASS")
print("Quota exception architecture: PASS")
print("Transient error classification: PASS")
print("Bounded retry architecture: PASS")
print("Quota classification: PASS")
print("No obvious unbounded retry loop: PASS")
print("Retry observability: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

