from pathlib import Path
import subprocess
import sys

print("=" * 80)
print("STEP 8C-004 — TASK 70 — SCANNER ALEMBIC MIGRATION REGRESSION")
print("=" * 80)

ROOT = Path(".").resolve()
ALEMBIC_INI = ROOT / "alembic.ini"
ALEMBIC_DIR = ROOT / "alembic"
VERSIONS_DIR = ALEMBIC_DIR / "versions"
MODEL_PATH = ROOT / "app" / "models" / "scan.py"
BASE_PATH = ROOT / "app" / "db" / "base.py"

print()
print("===== 1. VERIFY ALEMBIC ARCHITECTURE =====")

for required in [
    ALEMBIC_INI,
    ALEMBIC_DIR,
    VERSIONS_DIR,
]:
    if not required.exists():
        raise RuntimeError(
            f"Required Alembic component missing: {required}"
        )
    print(f"{required}: PRESENT")

print("Alembic architecture: PASS")

print()
print("===== 2. VERIFY SCANNER MODEL =====")

if not MODEL_PATH.exists():
    raise RuntimeError(
        "Scanner SQLAlchemy model missing: app/models/scan.py"
    )

model_text = MODEL_PATH.read_text(
    encoding="utf-8"
)

for marker in [
    'class Scan(Base):',
    '__tablename__ = "scans"',
    'ForeignKey(',
    '"users.id"',
    'visual_evidence',
    'alternative_matches',
]:
    if marker not in model_text:
        raise RuntimeError(
            f"Scanner model marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Scanner model: PASS")

print()
print("===== 3. VERIFY MODEL IS REGISTERED WITH SQLALCHEMY BASE =====")

base_text = BASE_PATH.read_text(
    encoding="utf-8"
)

if "models.scan" not in base_text and "from app.models.scan" not in base_text:
    print(
        "Scanner model import registration: NOT YET PRESENT"
    )
    print(
        "Migration autogeneration may not detect Scan automatically."
    )
else:
    print(
        "Scanner model import registration: PRESENT"
    )

print("Base registration inspection: COMPLETE")

print()
print("===== 4. INSPECT CURRENT ALEMBIC HEAD =====")

result = subprocess.run(
    ["alembic", "current"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
    raise RuntimeError(
        "Alembic current command failed. STOP."
    )

print("Alembic current: PASS")

current_output = (
    result.stdout
    + "\n"
    + result.stderr
).strip()

print(
    "Current migration state: DETECTED"
    if current_output
    else
    "Current migration state: EMPTY"
)

print()
print("===== 5. INSPECT ALEMBIC HEAD =====")

result = subprocess.run(
    ["alembic", "heads"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
    raise RuntimeError(
        "Alembic heads command failed. STOP."
    )

head_output = (
    result.stdout
    + "\n"
    + result.stderr
).strip()

if not head_output:
    raise RuntimeError(
        "No Alembic head detected. STOP."
    )

print("Alembic head: PRESENT")
print("Migration chain: PASS")

print()
print("===== 6. VERIFY NO SCANNER MIGRATION ALREADY EXISTS =====")

migration_files = list(
    VERSIONS_DIR.glob("*.py")
)

scanner_migrations = []

for migration in migration_files:
    text = migration.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if (
        'create_table("scans"' in text
        or "create_table('scans'" in text
        or "op.create_table(\n        \"scans\"" in text
        or "op.create_table(\n        'scans'" in text
    ):
        scanner_migrations.append(migration)

if scanner_migrations:
    print("Existing scanner migration: PRESENT")
    for migration in scanner_migrations:
        print(f"  -> {migration}")
    print("Migration creation: ALREADY PRESENT")
else:
    print("Existing scanner migration: NOT FOUND")
    print("Migration creation: REQUIRED")

print()
print("===== 7. VERIFY DATABASE SAFETY BOUNDARY =====")

for forbidden in [
    "image_bytes",
    "image_base64",
    "GEMINI_API_KEY",
    "access_token",
    "refresh_token",
    "response.text",
]:
    if forbidden in model_text:
        raise RuntimeError(
            f"Forbidden persistence field detected: {forbidden}"
        )

print("Raw image persistence: NOT PRESENT")
print("Base64 image persistence: NOT PRESENT")
print("Gemini response persistence: NOT PRESENT")
print("Credential persistence: NOT PRESENT")
print("Persistence safety: PASS")

print()
print("===== 8. VERIFY MIGRATION COMMAND AVAILABILITY =====")

result = subprocess.run(
    ["alembic", "--version"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    raise RuntimeError(
        "Alembic executable unavailable. STOP."
    )

print("Alembic executable: PASS")

print()
print("===== 9. MIGRATION DECISION GATE =====")

if scanner_migrations:
    print(
        "Scanner migration already exists."
    )
    print(
        "No duplicate migration will be created."
    )
else:
    print(
        "Scanner migration absent."
    )
    print(
        "Migration generation boundary: READY"
    )

print("Architecture decision gate: PASS")

print()
print("===== 10. PRODUCTION SAFETY =====")

print("Alembic architecture inspected: PASS")
print("Migration chain inspected: PASS")
print("Scanner model inspected: PASS")
print("Duplicate migration check: PASS")
print("No database migration executed by regression: PASS")
print("No database records mutated: PASS")
print("Real Gemini request: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")

print()
print("=" * 80)
print("TASK 70 COMPLETE")
print("=" * 80)
print("Alembic architecture: PASS")
print("Scanner model: PASS")
print("Migration chain: PASS")
print("Duplicate migration check: PASS")
print("Persistence safety: PASS")
print("READY FOR SCANNER MIGRATION GENERATION")
print("=" * 80)
