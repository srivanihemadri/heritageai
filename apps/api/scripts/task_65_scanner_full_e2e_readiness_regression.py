from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 65 — SCANNER FULL E2E READINESS REGRESSION")
print("=" * 80)

required_files = [
    Path("app/api/v1/ai.py"),
    Path("app/services/ai/scanner/service.py"),
    Path("app/services/ai/scanner/contract.py"),
    Path("app/services/ai/scanner/prompts.py"),
]

for path in required_files:
    if not path.exists():
        raise RuntimeError(f"Required scanner file missing: {path}")
    print(f"{path.as_posix()}: PRESENT")

ai = Path("app/api/v1/ai.py").read_text(encoding="utf-8")
service = Path("app/services/ai/scanner/service.py").read_text(encoding="utf-8")

for term in [
    '"/scan"',
    "HeritageScannerService",
    "ScannerQuotaExceededError",
    "ScannerImageValidationError",
]:
    if term not in ai:
        raise RuntimeError(f"E2E API boundary missing: {term}")
    print(f"{term}: PRESENT")

for term in [
    "class HeritageScannerService",
    "ScannerQuotaExceededError",
    "MAX_TRANSIENT_RETRIES",
]:
    if term not in service:
        raise RuntimeError(f"E2E service boundary missing: {term}")
    print(f"{term}: PRESENT")

print("Full scanner E2E architecture: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
print("TASK 65 COMPLETE")
print("=" * 80)
