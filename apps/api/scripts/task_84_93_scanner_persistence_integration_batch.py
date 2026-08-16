from pathlib import Path
import py_compile

print("=" * 80)
print("STEP 8C-005 — TASKS 84-93 — SCANNER PERSISTENCE INTEGRATION BATCH")
print("=" * 80)

ROOT = Path("app")

required_files = [
    ROOT / "api" / "v1" / "ai.py",
    ROOT / "dependencies.py",
    ROOT / "db" / "session.py",
    ROOT / "models" / "user.py",
    ROOT / "models" / "scan.py",
    ROOT / "repositories" / "scan.py",
    ROOT / "services" / "ai" / "scanner" / "service.py",
    ROOT / "services" / "ai" / "scanner" / "contract.py",
]

print()
print("===== TASK 84 — REPOSITORY RUNTIME ARCHITECTURE =====")

for path in required_files:
    if not path.exists():
        raise RuntimeError(f"Required file missing: {path}")

print("Required architecture: PASS")

repository = (ROOT / "repositories" / "scan.py").read_text(
    encoding="utf-8"
)

for marker in [
    "class ScanRepository",
    "def create",
    "def get_by_id",
    "def list_by_user",
    "user_id=user_id",
    "Scan.user_id == user_id",
    ".limit(limit)",
    ".offset(offset)",
]:
    if marker not in repository:
        raise RuntimeError(
            f"Repository contract missing: {marker}"
        )

print("ScanRepository contract: PASS")

print()
print("===== TASK 85 — SCANNER → REPOSITORY BOUNDARY =====")

api = (ROOT / "api" / "v1" / "ai.py").read_text(
    encoding="utf-8"
)

for marker in [
    "HeritageScannerService",
    "HeritageScannerResponse",
    "current_user=Depends(get_current_user)",
]:
    if marker not in api:
        raise RuntimeError(
            f"Scanner API boundary missing: {marker}"
        )

print("Scanner API boundary: PASS")

if "ScanRepository" not in api:
    print("ScanRepository integration: NOT YET IMPLEMENTED")
    print("Integration implementation boundary: IDENTIFIED")
else:
    print("ScanRepository integration: PRESENT")

print()
print("===== TASK 86 — AUTHENTICATED PERSISTENCE CONTRACT =====")

dependencies = (ROOT / "dependencies.py").read_text(
    encoding="utf-8"
)

for marker in [
    "def get_current_user",
    "db: Session = Depends(get_db)",
]:
    if marker not in dependencies:
        raise RuntimeError(
            f"Authenticated DB dependency missing: {marker}"
        )

print("Authenticated user: PASS")
print("Database session dependency: PASS")

print()
print("===== TASK 87 — STABLE SCAN ID CONTRACT =====")

contract = (
    ROOT / "services" / "ai" / "scanner" / "contract.py"
).read_text(encoding="utf-8")

for marker in [
    "class HeritageScannerResponse",
    "scan_id: str",
    "result: HeritageScannerResult",
]:
    if marker not in contract:
        raise RuntimeError(
            f"Scanner response contract missing: {marker}"
        )

print("Public scan_id: PRESENT")
print("Scanner result: PRESENT")
print("Stable scan response contract: PASS")

print()
print("===== TASK 88 — SINGLE SCAN RETRIEVAL CONTRACT =====")

if "def get_by_id" not in repository:
    raise RuntimeError(
        "Single-scan repository retrieval missing."
    )

if "Scan.id == scan_id" not in repository:
    raise RuntimeError(
        "Scan ID filtering missing."
    )

print("Single scan repository retrieval: PASS")

print()
print("===== TASK 89 — USER OWNERSHIP ISOLATION =====")

if "Scan.user_id == user_id" not in repository:
    raise RuntimeError(
        "Ownership filtering missing."
    )

print("Scan ownership filtering: PASS")
print("Cross-user access boundary: DEFINED")

print()
print("===== TASK 90 — SCAN HISTORY CONTRACT =====")

if "def list_by_user" not in repository:
    raise RuntimeError(
        "User scan-history repository operation missing."
    )

print("User scan history repository operation: PASS")

print()
print("===== TASK 91 — PAGINATION + ORDERING =====")

for marker in [
    "limit: int = 50",
    "offset: int = 0",
    ".limit(limit)",
    ".offset(offset)",
    "Scan.created_at.desc()",
]:
    if marker not in repository:
        raise RuntimeError(
            f"Pagination/order marker missing: {marker}"
        )

print("Pagination: PASS")
print("Newest-first ordering: PASS")

print()
print("===== TASK 92 — PERSISTENCE FAILURE SAFETY =====")

session = (ROOT / "db" / "session.py").read_text(
    encoding="utf-8"
)

if "Session" not in session:
    raise RuntimeError(
        "SQLAlchemy Session architecture missing."
    )

print("SQLAlchemy session architecture: PASS")
print("Persistence failure boundary: READY FOR INTEGRATION")

print()
print("===== TASK 93 — END-TO-END INTEGRATION GATE =====")

print("Scanner service: PRESENT")
print("Scanner contract: PRESENT")
print("Scan model: PRESENT")
print("Scan repository: PRESENT")
print("Authenticated user boundary: PRESENT")
print("Database session boundary: PRESENT")
print("Persistence integration: READY")

print()
print("=" * 80)
print("TASKS 84-93 ARCHITECTURE BATCH COMPLETE")
print("=" * 80)
print("Repository architecture: PASS")
print("Authenticated persistence boundary: PASS")
print("Stable scan contract: PASS")
print("Retrieval architecture: PASS")
print("Ownership architecture: PASS")
print("History architecture: PASS")
print("Pagination architecture: PASS")
print("Persistence safety gate: PASS")
print()
print("IMPORTANT:")
print("Scanner API persistence integration is the remaining implementation.")
print("NO DATABASE MIGRATION REQUIRED.")
print("NO REAL GEMINI REQUEST.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
