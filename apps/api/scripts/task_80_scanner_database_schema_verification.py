from sqlalchemy import inspect

from app.db.session import engine
from app.models.scan import Scan


print("=" * 80)
print("STEP 8C-004 — TASK 80 — SCANNER DATABASE SCHEMA VERIFICATION")
print("=" * 80)


print()
print("===== 1. DATABASE CONNECTION =====")

inspector = inspect(engine)

print("Database inspector: PASS")


print()
print("===== 2. VERIFY SCANS TABLE =====")

tables = inspector.get_table_names()

if "scans" not in tables:
    raise RuntimeError("scans table missing. STOP.")

print("scans table: PRESENT")
print("scans table: PASS")


print()
print("===== 3. VERIFY DATABASE COLUMNS =====")

columns = inspector.get_columns("scans")
db_columns = {column["name"]: column for column in columns}

required = [
    "id",
    "user_id",
    "identification_status",
    "evidence_quality",
    "identified_name",
    "category",
    "location",
    "country",
    "confidence",
    "confidence_level",
    "description",
    "architectural_style",
    "historical_period",
    "historical_significance",
    "visual_evidence",
    "alternative_matches",
    "grounding_status",
    "created_at",
    "updated_at",
]

for field in required:
    if field not in db_columns:
        raise RuntimeError(
            f"Missing database column: {field}"
        )

    print(f"{field}: PRESENT")

print("Database column contract: PASS")


print()
print("===== 4. VERIFY PRIMARY KEY =====")

pk = inspector.get_pk_constraint("scans")

print(
    "Primary key columns:",
    pk.get("constrained_columns"),
)

if pk.get("constrained_columns") != ["id"]:
    raise RuntimeError(
        "Invalid scans primary key. STOP."
    )

print("Primary key: PASS")


print()
print("===== 5. VERIFY FOREIGN KEY =====")

fks = inspector.get_foreign_keys("scans")

matching = [
    fk
    for fk in fks
    if (
        fk.get("referred_table") == "users"
        and fk.get("referred_columns") == ["id"]
        and fk.get("constrained_columns") == ["user_id"]
    )
]

if not matching:
    raise RuntimeError(
        "users.id foreign key missing. STOP."
    )

print("user_id -> users.id: PASS")


print()
print("===== 6. VERIFY INDEXES =====")

indexes = inspector.get_indexes("scans")

names = {
    index["name"]
    for index in indexes
}

if "ix_scans_user_id" not in names:
    raise RuntimeError(
        "ix_scans_user_id missing. STOP."
    )

if "ix_scans_user_id_created_at" not in names:
    raise RuntimeError(
        "ix_scans_user_id_created_at missing. STOP."
    )

print("ix_scans_user_id: PRESENT")
print("ix_scans_user_id_created_at: PRESENT")
print("Indexes: PASS")


print()
print("===== 7. VERIFY ORM METADATA =====")

print("Scan.__tablename__:", Scan.__tablename__)

if Scan.__tablename__ != "scans":
    raise RuntimeError(
        "ORM table mapping mismatch. STOP."
    )

print("ORM table mapping: PASS")


print()
print("===== 8. VERIFY EMPTY TABLE =====")

with engine.connect() as conn:
    count = conn.exec_driver_sql(
        "SELECT COUNT(*) FROM scans"
    ).scalar()

print("Existing scan records:", count)

if count != 0:
    raise RuntimeError(
        f"Expected empty scans table, found {count} records. STOP."
    )

print("Initial scan table state: EMPTY")


print()
print("===== 9. PRODUCTION SAFETY =====")

print("Schema inspection: PASS")
print("Database schema mutation: NONE")
print("Database records created: NONE")
print("Database records modified: NONE")
print("Real Gemini request: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")


print()
print("=" * 80)
print("TASK 80 COMPLETE")
print("=" * 80)

print("scans table: PASS")
print("Column contract: PASS")
print("Primary key: PASS")
print("User foreign key: PASS")
print("Indexes: PASS")
print("ORM mapping: PASS")
print("Initial table state: EMPTY")

print("READY FOR TASK 81 — SCANNER PERSISTENCE REPOSITORY")

print("=" * 80)
