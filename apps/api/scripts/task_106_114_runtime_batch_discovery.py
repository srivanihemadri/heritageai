from pathlib import Path

print("=" * 80)
print("STEP 8C-006 — TASKS 106-114 — RUNTIME BATCH DISCOVERY")
print("=" * 80)

targets = [
    Path("scripts/ai_heritage_scanner_real_api_smoke_test.py"),
    Path("scripts/ai_heritage_scanner_real_jwt_boundary_test.py"),
    Path("scripts/ai_heritage_scanner_controlled_test.png"),
    Path("app/api/v1/ai.py"),
    Path("app/repositories/scan.py"),
    Path("app/models/scan.py"),
    Path("app/services/ai/scanner/service.py"),
    Path("app/db/session.py"),
]

for path in targets:
    print()
    print("=" * 80)
    print(path)
    print("=" * 80)

    if not path.exists():
        print("MISSING")
        continue

    print(path.read_text(encoding="utf-8", errors="replace"))

print()
print("=" * 80)
print("TASKS 106-114 DISCOVERY COMPLETE")
print("=" * 80)
