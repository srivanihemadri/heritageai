from __future__ import annotations

import sys
from pathlib import Path
import inspect

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.image import validate_image_bytes


print("=" * 80)
print("STEP 8C-003 — TASK 17-RECOVERY — INSPECT MIME MISMATCH VALIDATION")
print("=" * 80)

print()
print("===== 1. VALIDATOR SOURCE =====")

print(inspect.getsource(validate_image_bytes))

print()
print("===== 2. TASK 17 FIXTURE =====")

fixture_path = (
    Path(__file__).resolve().parent
    / "task_17_scanner_negative_path_security_regression.py"
)

if not fixture_path.exists():
    raise RuntimeError(
        f"Task 17 regression script not found: {fixture_path}"
    )

source = fixture_path.read_text(encoding="utf-8")

lines = source.splitlines()

for number, line in enumerate(lines, start=1):
    if 175 <= number <= 210:
        print(f"{number:4}: {line}")

print()
print("===== 3. PRODUCTION SAFETY =====")

print("Read-only diagnostic: PASS")
print("Real Gemini request: NONE")
print("Database changes: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("TASK 17-RECOVERY DIAGNOSTIC COMPLETE")
print("=" * 80)
