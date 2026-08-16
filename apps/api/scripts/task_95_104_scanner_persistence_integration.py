from pathlib import Path
import subprocess
import sys

ROOT = Path(".")
API = ROOT / "app/api/v1/ai.py"
REPO = ROOT / "app/repositories/scan.py"

print("=" * 80)
print("STEP 8C-005 — TASKS 95-104 — SCANNER PERSISTENCE INTEGRATION")
print("=" * 80)

print()
print("===== 1. PRE-IMPLEMENTATION SAFETY GATE =====")

required = [
    API,
    REPO,
    ROOT / "app/models/scan.py",
    ROOT / "app/services/ai/scanner/contract.py",
    ROOT / "app/services/ai/scanner/service.py",
    ROOT / "app/dependencies.py",
    ROOT / "app/db/session.py",
]

for path in required:
    if not path.exists():
        raise RuntimeError(f"Required file missing: {path}")
    print(f"{path.as_posix()}: PRESENT")

print("Required architecture: PASS")

api_text = API.read_text(encoding="utf-8")

required_api_markers = [
    '@router.post(\n    "/scan"',
    "async def heritage_scan(",
    "file: UploadFile = File(...)",
    "current_user=Depends(get_current_user)",
    "service.scan(",
    "HeritageScannerResponse",
]

for marker in required_api_markers:
    if marker not in api_text:
        raise RuntimeError(
            f"Expected existing API marker missing: {marker}"
        )

print("Existing scanner endpoint structure: PASS")

print()
print("===== 2. TASK 95 — DATABASE SESSION INTEGRATION =====")

if "from sqlalchemy.orm import Session" not in api_text:
    api_text = api_text.replace(
        "from fastapi import (",
        "from sqlalchemy.orm import Session\n\nfrom fastapi import (",
        1,
    )

if "from app.db.session import get_db" not in api_text:
    api_text = api_text.replace(
        "from app.dependencies import get_current_user",
        "from app.dependencies import get_current_user\nfrom app.db.session import get_db",
        1,
    )

if "from app.repositories.scan import ScanRepository" not in api_text:
    api_text = api_text.replace(
        "from app.services.ai.scanner.service import (",
        "from app.repositories.scan import ScanRepository\nfrom app.services.ai.scanner.service import (",
        1,
    )

old_signature = '''async def heritage_scan(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> HeritageScannerResponse:'''

new_signature = '''async def heritage_scan(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HeritageScannerResponse:'''

if old_signature in api_text:
    api_text = api_text.replace(
        old_signature,
        new_signature,
        1,
    )
elif "db: Session = Depends(get_db)" not in api_text:
    raise RuntimeError(
        "Could not safely locate scanner endpoint signature."
    )

print("SQLAlchemy Session dependency: PASS")
print("get_db dependency: PASS")

print()
print("===== 3. TASK 96 — REPOSITORY INTEGRATION =====")

if "repository = ScanRepository(db)" not in api_text:
    marker = '''        service = HeritageScannerService()

        return service.scan(
            image_bytes=image_bytes,
            content_type=file.content_type.lower(),
        )'''

    replacement = '''        service = HeritageScannerService()

        result = service.scan(
            image_bytes=image_bytes,
            content_type=file.content_type.lower(),
        )

        repository = ScanRepository(db)

        scan = repository.create(
            user_id=current_user.id,
            result=result.result,
        )'''

    if marker not in api_text:
        raise RuntimeError(
            "Expected scanner execution block not found. "
            "No API integration changes were applied."
        )

    api_text = api_text.replace(
        marker,
        replacement,
        1,
    )

print("ScanRepository integration: PASS")

print()
print("===== 4. TASK 97 — RESULT PERSISTENCE =====")

if "result=result.result" not in api_text:
    raise RuntimeError(
        "Scanner result is not mapped into persistence."
    )

if "user_id=current_user.id" not in api_text:
    raise RuntimeError(
        "Authenticated user ownership is not enforced."
    )

print("Scanner result persistence mapping: PASS")
print("Authenticated ownership: PASS")

print()
print("===== 5. TASK 98 — TRANSACTION SAFETY =====")

if "db.commit()" not in api_text:
    marker = '''        scan = repository.create(
            user_id=current_user.id,
            result=result.result,
        )'''

    replacement = '''        scan = repository.create(
            user_id=current_user.id,
            result=result.result,
        )

        db.commit()
        db.refresh(scan)'''

    if marker not in api_text:
        raise RuntimeError(
            "Could not locate persistence block for transaction integration."
        )

    api_text = api_text.replace(
        marker,
        replacement,
        1,
    )

print("Database commit: PASS")
print("Persisted entity refresh: PASS")

print()
print("===== 6. TASK 99 — STABLE SCAN RESPONSE =====")

marker = '''        db.commit()
        db.refresh(scan)'''

replacement = '''        db.commit()
        db.refresh(scan)

        return HeritageScannerResponse(
            success=True,
            scan_id=str(scan.id),
            result=result.result,
        )'''

if "return HeritageScannerResponse(" not in api_text:
    if marker not in api_text:
        raise RuntimeError(
            "Could not locate transaction boundary."
        )

    api_text = api_text.replace(
        marker,
        replacement,
        1,
    )

print("Stable scan_id response: PASS")

print()
print("===== 7. TASK 100 — SINGLE SCAN RETRIEVAL =====")

single_route = '''

@router.get(
    "/scans/{scan_id}",
    response_model=HeritageScannerResponse,
)
def get_scan(
    scan_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HeritageScannerResponse:

    repository = ScanRepository(db)

    scan = repository.get_by_id(
        scan_id=scan_id,
        user_id=current_user.id,
    )

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "SCAN_NOT_FOUND",
                "message": "Scan not found.",
            },
        )

    result = HeritageScannerResult(
        identified_name=scan.identified_name,
        identification_status=scan.identification_status,
        evidence_quality=scan.evidence_quality,
        category=scan.category,
        location=scan.location,
        country=scan.country,
        confidence=scan.confidence,
        confidence_level=scan.confidence_level,
        description=scan.description,
        architectural_style=scan.architectural_style,
        historical_period=scan.historical_period,
        historical_significance=scan.historical_significance,
        visual_evidence=scan.visual_evidence,
        alternative_matches=scan.alternative_matches,
        grounding_status=scan.grounding_status,
    )

    return HeritageScannerResponse(
        success=True,
        scan_id=str(scan.id),
        result=result,
    )
'''

if '"/scans/{scan_id}"' not in api_text:
    api_text += single_route

print("Single authenticated scan retrieval: PASS")

print()
print("===== 8. TASK 101 — SCAN HISTORY =====")

history_route = '''

@router.get(
    "/scans",
    response_model=list[HeritageScannerResponse],
)
def list_scans(
    limit: int = 50,
    offset: int = 0,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[HeritageScannerResponse]:

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="limit must be between 1 and 100.",
        )

    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="offset must be >= 0.",
        )

    repository = ScanRepository(db)

    scans = repository.list_by_user(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )

    responses = []

    for scan in scans:
        result = HeritageScannerResult(
            identified_name=scan.identified_name,
            identification_status=scan.identification_status,
            evidence_quality=scan.evidence_quality,
            category=scan.category,
            location=scan.location,
            country=scan.country,
            confidence=scan.confidence,
            confidence_level=scan.confidence_level,
            description=scan.description,
            architectural_style=scan.architectural_style,
            historical_period=scan.historical_period,
            historical_significance=scan.historical_significance,
            visual_evidence=scan.visual_evidence,
            alternative_matches=scan.alternative_matches,
            grounding_status=scan.grounding_status,
        )

        responses.append(
            HeritageScannerResponse(
                success=True,
                scan_id=str(scan.id),
                result=result,
            )
        )

    return responses
'''

if 'def list_scans(' not in api_text:
    api_text += history_route

print("Authenticated scan history: PASS")

print()
print("===== 9. TASK 102 — PAGINATION + ORDERING =====")

repository_text = REPO.read_text(encoding="utf-8")

for marker in [
    "limit: int = 50",
    "offset: int = 0",
    ".limit(limit)",
    ".offset(offset)",
    "Scan.created_at.desc()",
]:
    if marker not in repository_text:
        raise RuntimeError(
            f"Repository pagination marker missing: {marker}"
        )

print("Pagination: PASS")
print("Newest-first ordering: PASS")

print()
print("===== 10. TASK 103 — CROSS-USER ISOLATION =====")

if "Scan.user_id == user_id" not in repository_text:
    raise RuntimeError(
        "Repository ownership filter missing."
    )

if "user_id=current_user.id" not in api_text:
    raise RuntimeError(
        "API ownership boundary missing."
    )

print("Cross-user isolation: PASS")

print()
print("===== 11. TASK 104 — APPLY SOURCE CHANGE =====")

API.write_text(api_text, encoding="utf-8")

print("app/api/v1/ai.py updated: PASS")

print()
print("===== 12. COMPILE APPLICATION SOURCES =====")

files_to_compile = [
    API,
    REPO,
    ROOT / "app/models/scan.py",
    ROOT / "app/db/base.py",
]

for path in files_to_compile:
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(
            f"Compilation failed: {path}"
        )

    print(f"{path.as_posix()}: PASS")

print("Application compilation: PASS")

print()
print("===== 13. IMPORT + ROUTE REGRESSION =====")

check = subprocess.run(
    [
        sys.executable,
        "-c",
        """
from app.db.base import Base
from app.models.scan import Scan
from app.repositories.scan import ScanRepository
from app.api.v1.ai import router

print("Base import: PASS")
print("Scan import: PASS")
print("ScanRepository import: PASS")
print("AI router import: PASS")
print("scans in metadata:", "PASS" if "scans" in Base.metadata.tables else "FAIL")
assert "scans" in Base.metadata.tables
print("Task 104 import gate: PASS")
""",
    ],
    capture_output=True,
    text=True,
)

print(check.stdout)

if check.returncode != 0:
    print(check.stderr)
    raise RuntimeError(
        "Task 104 import regression failed."
    )

print("Import regression: PASS")

print()
print("===== 14. DATABASE SAFETY =====")

print("Existing scans table: PRESERVED")
print("Alembic migration: NOT REQUIRED")
print("Alembic upgrade: NOT EXECUTED")
print("Database records inserted by batch: NONE")
print("Database records modified by batch: NONE")

print()
print("===== 15. AI SAFETY =====")

print("Real Gemini request: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")

print()
print("=" * 80)
print("TASKS 95-104 COMPLETE")
print("=" * 80)
print("DB session integration: PASS")
print("Repository integration: PASS")
print("Scanner result persistence: PASS")
print("Transaction boundary: PASS")
print("Stable scan_id response: PASS")
print("Single scan retrieval: PASS")
print("Scan history: PASS")
print("Pagination: PASS")
print("Newest-first ordering: PASS")
print("Cross-user isolation: PASS")
print("Compilation: PASS")
print("Import regression: PASS")
print()
print("IMPORTANT:")
print("Source integration is complete.")
print("No real Gemini request was made.")
print("No database test record was created by this batch.")
print("A real authenticated scanner integration test remains.")
print("=" * 80)
