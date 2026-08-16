from pathlib import Path

print("=" * 80)
print("STEP 8C-004 — TASK 71 — SCANNER MODEL REGISTRATION REGRESSION")
print("=" * 80)

BASE = Path("app/db/base.py")
SCAN = Path("app/models/scan.py")
ALEMBIC_ENV = Path("alembic/env.py")

print()
print("===== 1. VERIFY SCANNER MODEL =====")

if not SCAN.exists():
    raise RuntimeError(
        "app/models/scan.py is missing. STOP."
    )

scan_text = SCAN.read_text(
    encoding="utf-8"
)

for marker in [
    "class Scan(Base):",
    '__tablename__ = "scans"',
    '"users.id"',
]:
    if marker not in scan_text:
        raise RuntimeError(
            f"Scanner model marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Scanner model: PASS")

print()
print("===== 2. INSPECT SQLALCHEMY BASE REGISTRATION =====")

if not BASE.exists():
    raise RuntimeError(
        "app/db/base.py is missing. STOP."
    )

base_text = BASE.read_text(
    encoding="utf-8"
)

print("app/db/base.py: PRESENT")

if "models.scan" in base_text or "app.models.scan" in base_text:
    print("Scanner model registration: PRESENT")
    already_registered = True
else:
    print("Scanner model registration: NOT PRESENT")
    already_registered = False

print()
print("===== 3. INSPECT ALEMBIC MODEL DISCOVERY =====")

if not ALEMBIC_ENV.exists():
    raise RuntimeError(
        "alembic/env.py is missing. STOP."
    )

env_text = ALEMBIC_ENV.read_text(
    encoding="utf-8"
)

for marker in [
    "target_metadata",
    "Base.metadata",
]:
    if marker not in env_text:
        raise RuntimeError(
            f"Alembic metadata marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Alembic metadata architecture: PASS")

print()
print("===== 4. VERIFY SCANNER MODEL IMPORTABILITY =====")

import sys

api_root = Path(".").resolve()

if str(api_root) not in sys.path:
    sys.path.insert(0, str(api_root))

try:
    from app.models.scan import Scan
except Exception as exc:
    raise RuntimeError(
        f"Scanner model import failed: {type(exc).__name__}"
    ) from exc

print("from app.models.scan import Scan: PASS")

if Scan.__tablename__ != "scans":
    raise RuntimeError(
        "Scan model table name is not scans."
    )

print("Scan.__tablename__: scans")
print("Scanner model importability: PASS")

print()
print("===== 5. VERIFY METADATA REGISTRATION =====")

try:
    from app.db.base import Base
except Exception as exc:
    raise RuntimeError(
        f"Base import failed: {type(exc).__name__}"
    ) from exc

if "scans" in Base.metadata.tables:
    print("scans table in Base.metadata: PRESENT")
else:
    print("scans table in Base.metadata: NOT PRESENT")

print()
print("===== 6. APPLY REGISTRATION ONLY IF REQUIRED =====")

if already_registered:
    print(
        "Scanner model already registered."
    )
    print(
        "No source modification required."
    )
else:
    print(
        "Scanner model registration is required."
    )
    print(
        "This regression intentionally does NOT modify production source."
    )
    print(
        "Registration implementation boundary: IDENTIFIED"
    )

print()
print("===== 7. MIGRATION SAFETY GATE =====")

print(
    "Alembic migration generation: NOT EXECUTED"
)
print(
    "Alembic upgrade: NOT EXECUTED"
)
print(
    "Database mutation: NONE"
)

print()
print("===== 8. PRODUCTION SAFETY =====")

print("Scanner model inspection: PASS")
print("Alembic metadata inspection: PASS")
print("Registration boundary: IDENTIFIED")
print("No migration generated: PASS")
print("No database mutation: PASS")
print("Real Gemini request: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")

print()
print("=" * 80)
print("TASK 71 COMPLETE")
print("=" * 80)
print("Scanner model: PASS")
print("Alembic metadata: PASS")
print("Registration status: INSPECTED")
print("Migration safety gate: PASS")
print("READY FOR REGISTRATION IMPLEMENTATION")
print("=" * 80)
