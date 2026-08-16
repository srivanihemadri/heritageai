from pathlib import Path

print("=" * 80)
print("STEP 8C-006 — TASK 105 — ORM REGISTRATION ARCHITECTURE AUDIT")
print("=" * 80)

print()
print("===== BASE.PY =====")
print(Path("app/db/base.py").read_text(encoding="utf-8"))

print()
print("===== ALEMBIC ENV.PY =====")
print(Path("alembic/env.py").read_text(encoding="utf-8"))

print()
print("===== APP ENTRYPOINT CANDIDATES =====")

candidates = [
    "app/main.py",
    "app/__init__.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
]

for candidate in candidates:
    path = Path(candidate)

    if path.exists():
        print(f"===== {candidate} =====")
        print(path.read_text(encoding="utf-8"))

print()
print("===== MODEL PACKAGE =====")

model_files = [
    path
    for path in Path("app/models").rglob("*.py")
    if "__pycache__" not in path.parts
]

for path in sorted(model_files):
    print(path)

print()
print("=" * 80)
print("TASK 105 AUDIT COMPLETE")
print("=" * 80)
