from pathlib import Path
from sqlalchemy.orm import Session

from app.db.session import engine
from app.models.scan import Scan
from app.repositories.scan import ScanRepository
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-004 — TASK 83 — SCANNER PERSISTENCE REPOSITORY UNIT REGRESSION")
print("=" * 80)


print()
print("===== 1. VERIFY REPOSITORY =====")

repository_path = Path("app/repositories/scan.py")

if not repository_path.exists():
    raise RuntimeError(
        "ScanRepository implementation missing. STOP."
    )

print("app/repositories/scan.py: PRESENT")
print("ScanRepository: PRESENT")


print()
print("===== 2. VERIFY DATABASE TABLE =====")

with engine.connect() as connection:
    result = connection.exec_driver_sql(
        "SELECT COUNT(*) FROM scans"
    ).scalar()

print(f"Existing scan records before test: {result}")
print("Database connection: PASS")


print()
print("===== 3. BUILD CONTROLLED SCANNER RESULT =====")

result = HeritageScannerResult.model_validate(
    {
        "identified_name": "Konark Sun Temple",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
        "category": "Temple",
        "location": "Konark",
        "country": "India",
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "description": "Controlled repository regression result.",
        "architectural_style": "Kalinga architecture",
        "historical_period": "13th century",
        "historical_significance": "Controlled historical significance.",
        "visual_evidence": [
            "Monumental stone temple structure",
            "Wheel-shaped architectural elements",
        ],
        "alternative_matches": [
            "Controlled alternative candidate",
        ],
        "grounding_status": "GROUNDED",
    }
)

print("HeritageScannerResult: PASS")
print("Structured visual evidence: PASS")
print("Structured alternatives: PASS")


print()
print("===== 4. CREATE CONTROLLED REPOSITORY RECORD =====")

test_user_id = "00000000-0000-0000-0000-000000000001"

with Session(engine) as session:
    repository = ScanRepository(session)

    scan = repository.create(
        user_id=test_user_id,
        result=result,
    )

    scan_id = str(scan.id)

    if not scan.id:
        raise RuntimeError(
            "Repository create() did not produce scan ID."
        )

    if scan.user_id != test_user_id:
        raise RuntimeError(
            "Repository create() lost user ownership."
        )

    session.rollback()

print("Repository create(): PASS")
print("Scan ID generation: PASS")
print("User ownership assignment: PASS")
print("Transaction rollback: PASS")


print()
print("===== 5. VERIFY CREATE MAPPING =====")

with Session(engine) as session:
    repository = ScanRepository(session)

    scan = repository.create(
        user_id=test_user_id,
        result=result,
    )

    if scan.identification_status != result.identification_status:
        raise RuntimeError("identification_status mapping failed.")

    if scan.evidence_quality != result.evidence_quality:
        raise RuntimeError("evidence_quality mapping failed.")

    if scan.identified_name != result.identified_name:
        raise RuntimeError("identified_name mapping failed.")

    if scan.category != result.category:
        raise RuntimeError("category mapping failed.")

    if scan.location != result.location:
        raise RuntimeError("location mapping failed.")

    if scan.country != result.country:
        raise RuntimeError("country mapping failed.")

    if scan.confidence != result.confidence:
        raise RuntimeError("confidence mapping failed.")

    if scan.confidence_level != result.confidence_level:
        raise RuntimeError("confidence_level mapping failed.")

    if scan.description != result.description:
        raise RuntimeError("description mapping failed.")

    if scan.architectural_style != result.architectural_style:
        raise RuntimeError("architectural_style mapping failed.")

    if scan.historical_period != result.historical_period:
        raise RuntimeError("historical_period mapping failed.")

    if scan.historical_significance != result.historical_significance:
        raise RuntimeError("historical_significance mapping failed.")

    if scan.visual_evidence != result.visual_evidence:
        raise RuntimeError("visual_evidence mapping failed.")

    if scan.alternative_matches != result.alternative_matches:
        raise RuntimeError("alternative_matches mapping failed.")

    if scan.grounding_status != result.grounding_status:
        raise RuntimeError("grounding_status mapping failed.")

    persisted_scan_id = str(scan.id)

    session.commit()

print("Scanner field mapping: PASS")
print("Structured evidence persistence: PASS")
print("Structured alternatives persistence: PASS")
print("Database commit: PASS")


print()
print("===== 6. VERIFY GET BY ID =====")

with Session(engine) as session:
    repository = ScanRepository(session)

    fetched = repository.get_by_id(
        scan_id=persisted_scan_id,
        user_id=test_user_id,
    )

    if fetched is None:
        raise RuntimeError(
            "get_by_id() failed to retrieve persisted scan."
        )

    if str(fetched.id) != persisted_scan_id:
        raise RuntimeError(
            "get_by_id() returned incorrect scan."
        )

print("get_by_id(): PASS")
print("Persisted record retrieval: PASS")


print()
print("===== 7. VERIFY OWNERSHIP ISOLATION =====")

wrong_user_id = "00000000-0000-0000-0000-000000000002"

with Session(engine) as session:
    repository = ScanRepository(session)

    unauthorized = repository.get_by_id(
        scan_id=persisted_scan_id,
        user_id=wrong_user_id,
    )

    if unauthorized is not None:
        raise RuntimeError(
            "Ownership isolation failure: another user can retrieve scan."
        )

print("Wrong-user retrieval: NONE")
print("Ownership isolation: PASS")


print()
print("===== 8. VERIFY LIST BY USER =====")

with Session(engine) as session:
    repository = ScanRepository(session)

    records = repository.list_by_user(
        user_id=test_user_id,
        limit=50,
        offset=0,
    )

    matching = [
        record
        for record in records
        if str(record.id) == persisted_scan_id
    ]

    if not matching:
        raise RuntimeError(
            "list_by_user() did not return persisted scan."
        )

print("list_by_user(): PASS")
print("User-scoped listing: PASS")


print()
print("===== 9. VERIFY WRONG USER LIST =====")

with Session(engine) as session:
    repository = ScanRepository(session)

    records = repository.list_by_user(
        user_id=wrong_user_id,
        limit=50,
        offset=0,
    )

    if any(
        str(record.id) == persisted_scan_id
        for record in records
    ):
        raise RuntimeError(
            "Wrong user received another user's scan."
        )

print("Wrong-user list isolation: PASS")


print()
print("===== 10. VERIFY PAGINATION BOUNDARY =====")

with Session(engine) as session:
    repository = ScanRepository(session)

    records = repository.list_by_user(
        user_id=test_user_id,
        limit=1,
        offset=0,
    )

    if len(records) > 1:
        raise RuntimeError(
            "Repository pagination exceeded requested limit."
        )

print("Limit enforcement: PASS")


print()
print("===== 11. CLEAN CONTROLLED TEST DATA =====")

with Session(engine) as session:
    scan = session.get(
        Scan,
        persisted_scan_id,
    )

    if scan is not None:
        session.delete(scan)
        session.commit()

print("Controlled test record deleted: PASS")


print()
print("===== 12. VERIFY DATABASE CLEANUP =====")

with engine.connect() as connection:
    remaining = connection.exec_driver_sql(
        "SELECT COUNT(*) FROM scans WHERE id = %s",
        (persisted_scan_id,),
    ).scalar()

if remaining != 0:
    raise RuntimeError(
        "Controlled test scan was not cleaned up."
    )

print("Test record remaining: 0")
print("Database cleanup: PASS")


print()
print("===== 13. PRODUCTION SAFETY =====")

print("Repository runtime regression: PASS")
print("Controlled database records: USED")
print("Controlled test data cleanup: PASS")
print("Real Gemini request: NONE")
print("Gemini scanner execution: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production scanner endpoint: NOT CALLED")


print()
print("=" * 80)
print("TASK 83 COMPLETE")
print("=" * 80)

print("Repository create(): PASS")
print("Repository get_by_id(): PASS")
print("Repository list_by_user(): PASS")
print("Scanner result mapping: PASS")
print("Ownership isolation: PASS")
print("Wrong-user isolation: PASS")
print("Pagination: PASS")
print("Database cleanup: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("READY FOR TASK 84 — SCANNER PERSISTENCE SERVICE")
print("=" * 80)
