from pathlib import Path

print("=" * 80)
print("STEP 8C-006 — TASKS 106-114 — AUTHENTICATION RUNTIME DISCOVERY")
print("=" * 80)

targets = [
    Path("app/api/v1/auth.py"),
    Path("app/api/v1/users.py"),
    Path("app/models/user.py"),
    Path("app/db/session.py"),
    Path("app/core/config.py"),
    Path("tests/test_users.py"),
]

for path in targets:
    print()
    print("=" * 80)
    print(path)
    print("=" * 80)

    if path.exists():
        print(path.read_text(encoding="utf-8", errors="replace"))
    else:
        print("MISSING")

print()
print("=" * 80)
print("TASKS 106-114 AUTH DISCOVERY COMPLETE")
print("=" * 80)
