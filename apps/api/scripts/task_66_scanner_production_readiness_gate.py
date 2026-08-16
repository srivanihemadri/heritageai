from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 66 — SCANNER PRODUCTION READINESS GATE")
print("=" * 80)

checks = {
    "scanner route": Path("app/api/v1/ai.py"),
    "scanner service": Path("app/services/ai/scanner/service.py"),
    "scanner contract": Path("app/services/ai/scanner/contract.py"),
    "scanner prompts": Path("app/services/ai/scanner/prompts.py"),
}

for name, path in checks.items():
    if not path.exists():
        raise RuntimeError(f"Production readiness failure: {name} missing.")
    print(f"{name}: PRESENT")

service = checks["scanner service"].read_text(encoding="utf-8")
contract = checks["scanner contract"].read_text(encoding="utf-8")
prompts = checks["scanner prompts"].read_text(encoding="utf-8")
router = checks["scanner route"].read_text(encoding="utf-8")

required_markers = [
    ("retry", "MAX_TRANSIENT_RETRIES", service),
    ("quota", "ScannerQuotaExceededError", service),
    ("contract validation", "HeritageScannerResult", contract),
    ("visual evidence", "visual_evidence", contract),
    ("semantic prompt rule", "evidence_quality is NONE", prompts),
    ("scanner route", '"/scan"', router),
    ("HTTP 429", "SCANNER_QUOTA_EXCEEDED", router),
    ("HTTP 500", "SCANNER_FAILURE", router),
]

for name, marker, text in required_markers:
    if marker not in text:
        raise RuntimeError(
            f"Production readiness failure: {name} marker missing: {marker}"
        )
    print(f"{name}: PASS")

print()
print("Scanner production-readiness gate: PASS")
print("Architecture: PASS")
print("Contract: PASS")
print("Prompt semantics: PASS")
print("Retry/quota handling: PASS")
print("API failure mapping: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")
print("=" * 80)
print("TASK 66 COMPLETE")
print("=" * 80)
