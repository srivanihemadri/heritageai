from pathlib import Path

print("=" * 80)
print("STEP 8C-004 — TASK 67 — SCANNER PERSISTENCE ARCHITECTURE INSPECTION")
print("=" * 80)

root = Path("app")

print()
print("===== 1. DISCOVER DATABASE ARCHITECTURE =====")

database_terms = [
    "sqlalchemy",
    "create_engine",
    "AsyncSession",
    "Session",
    "DeclarativeBase",
    "Base",
    "mapped_column",
    "relationship",
]

database_files = []

for path in root.rglob("*.py"):
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if any(term in text for term in database_terms):
        database_files.append(path)

print(f"Database-related Python files: {len(database_files)}")

for path in database_files:
    print(f"PRESENT: {path.as_posix()}")

print()
print("===== 2. DISCOVER EXISTING MODELS =====")

model_terms = [
    "class User",
    "class Document",
    "class Chunk",
    "class Conversation",
    "class Scan",
    "class Scanner",
]

model_hits = {}

for path in database_files:
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    for term in model_terms:
        if term in text:
            model_hits.setdefault(term, []).append(
                path.as_posix()
            )

for term in model_terms:
    if term in model_hits:
        print(f"{term}: PRESENT")
        for path in model_hits[term]:
            print(f"  -> {path}")
    else:
        print(f"{term}: NOT FOUND")

print()
print("===== 3. DISCOVER MIGRATION ARCHITECTURE =====")

migration_roots = [
    Path("alembic"),
    Path("migrations"),
]

migration_found = False

for migration_root in migration_roots:
    if migration_root.exists():
        migration_found = True
        print(f"PRESENT: {migration_root.as_posix()}")

        for path in migration_root.rglob("*"):
            if path.is_file():
                print(f"  -> {path.as_posix()}")

if not migration_found:
    print("Migration directory: NOT FOUND")

print()
print("===== 4. DISCOVER REPOSITORY/DATA ACCESS LAYER =====")

repository_terms = [
    "repository",
    "repositories",
    "get_db",
    "get_session",
    "AsyncSession",
    "Session",
]

repository_files = []

for path in root.rglob("*.py"):
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    ).lower()

    if any(term.lower() in text for term in repository_terms):
        repository_files.append(path)

print(f"Relevant data-access files: {len(repository_files)}")

for path in repository_files:
    print(f"PRESENT: {path.as_posix()}")

print()
print("===== 5. DISCOVER EXISTING SCAN PERSISTENCE =====")

scan_terms = [
    "scan_id",
    "scan_history",
    "scanner_result",
    "HeritageScannerResult",
    "HeritageScannerResponse",
]

scan_hits = {}

for path in root.rglob("*.py"):
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    for term in scan_terms:
        if term in text:
            scan_hits.setdefault(term, []).append(
                path.as_posix()
            )

for term in scan_terms:
    if term in scan_hits:
        print(f"{term}: PRESENT")
        for path in scan_hits[term]:
            print(f"  -> {path}")
    else:
        print(f"{term}: NOT FOUND")

print()
print("===== 6. DISCOVER EXISTING DATABASE TABLE REFERENCES =====")

table_terms = [
    "__tablename__",
    "Table(",
    "ForeignKey(",
]

table_files = []

for path in root.rglob("*.py"):
    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if any(term in text for term in table_terms):
        table_files.append(path)

print(f"ORM/table-definition files: {len(table_files)}")

for path in table_files:
    print(f"PRESENT: {path.as_posix()}")

print()
print("===== 7. SCANNER INTEGRATION BOUNDARY =====")

scanner_service = Path(
    "app/services/ai/scanner/service.py"
)

scanner_contract = Path(
    "app/services/ai/scanner/contract.py"
)

scanner_router = Path(
    "app/api/v1/ai.py"
)

for path in [
    scanner_service,
    scanner_contract,
    scanner_router,
]:
    if not path.exists():
        raise RuntimeError(
            f"Required scanner file missing: {path}"
        )

    print(f"{path.as_posix()}: PRESENT")

print()
print("===== 8. ARCHITECTURE DECISION GATE =====")

print("Existing database architecture: INSPECTED")
print("Existing model architecture: INSPECTED")
print("Existing migration architecture: INSPECTED")
print("Existing repository architecture: INSPECTED")
print("Existing scanner persistence: INSPECTED")
print("No schema assumptions made: PASS")
print("No database mutations performed: PASS")

print()
print("===== 9. PRODUCTION SAFETY =====")

print("Database inspection only: PASS")
print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("TASK 67 COMPLETE")
print("=" * 80)
print("Database architecture: INSPECTED")
print("Model architecture: INSPECTED")
print("Migration architecture: INSPECTED")
print("Repository architecture: INSPECTED")
print("Scanner persistence boundary: INSPECTED")
print("READY FOR TASK 68 DESIGN")
print("=" * 80)
