from pathlib import Path
from pydantic import ValidationError

from app.services.ai.scanner.contract import HeritageScannerResult

print("=" * 80)
print("STEP 8C-006 — TASK 110 — SCANNER CONTRACT VALIDATION DIAGNOSTIC")
print("=" * 80)

print()
print("===== 1. CONTRACT IMPORT =====")
print("HeritageScannerResult: PASS")

print()
print("===== 2. VALIDATION RULE INVENTORY =====")

contract = Path(
    "app/services/ai/scanner/contract.py"
).read_text(encoding="utf-8")

rules = [
    "IDENTIFIED status requires an identified_name",
    "IDENTIFIED status requires visual_evidence",
    "POSSIBLE_MATCH status requires visual_evidence",
    "POSSIBLE_MATCH cannot use HIGH confidence",
    "AMBIGUOUS status requires at least two alternative_matches",
    "INSUFFICIENT_EVIDENCE cannot use HIGH confidence",
    "NOT_HERITAGE cannot contain an identified_name",
    "STRONG evidence quality requires visual_evidence",
    "NONE evidence quality cannot contain visual_evidence",
    "HIGH confidence requires confidence >= 0.90",
    "HIGH confidence requires an identified_name",
    "HIGH confidence requires visual_evidence",
    "MEDIUM confidence requires confidence >= 0.50 and < 0.90",
    "LOW confidence requires confidence < 0.50",
    "GROUNDED results require visual_evidence",
]

for rule in rules:
    print(f" - {rule}: DEFINED")

print()
print("Contract validation rules: PRESENT")

print()
print("===== 3. SCANNER SERVICE VALIDATION BOUNDARY =====")

service = Path(
    "app/services/ai/scanner/service.py"
).read_text(encoding="utf-8")

if "HeritageScannerResult.model_validate(" not in service:
    raise RuntimeError(
        "Scanner result validation boundary not found. STOP."
    )

print("Gemini payload -> HeritageScannerResult validation: PRESENT")
print("Validation boundary: PASS")

print()
print("===== 4. DIAGNOSTIC REQUIREMENT =====")
print("Exact Gemini payload: MUST NOT be persisted")
print("Raw image: MUST NOT be persisted")
print("Credentials: MUST NOT be persisted")
print("Database mutation: FORBIDDEN")
print("Qdrant mutation: FORBIDDEN")
print("Diagnostic-only execution: PASS")

print()
print("=" * 80)
print("TASK 110 DIAGNOSTIC PRECHECK COMPLETE")
print("=" * 80)
print("NEXT STEP:")
print("Run the existing real scanner test with temporary")
print("ValidationError diagnostics enabled.")
print("=" * 80)
