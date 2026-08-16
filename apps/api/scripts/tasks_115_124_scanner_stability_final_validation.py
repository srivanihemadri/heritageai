from pathlib import Path
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

print("=" * 80)
print("STEP 8C-006 — TASKS 115-124 — SCANNER STABILITY + FINAL VALIDATION")
print("=" * 80)

# ============================================================================
# TASK 115 — SOURCE + IMPORT GATE
# ============================================================================
print()
print("===== TASK 115 — APPLICATION IMPORT GATE =====")

sources = [
    "app/db/base.py",
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/scan.py",
    "app/models/heritage_site.py",
    "app/models/heritage_site_historical_event.py",
    "app/models/heritage_site_media.py",
    "app/models/heritage_site_metadata.py",
    "app/models/heritage_site_relation.py",
    "app/models/heritage_site_source.py",
    "app/models/ai/knowledge_document.py",
    "app/models/ai/knowledge_chunk.py",
    "app/models/ai/embedding.py",
    "app/repositories/scan.py",
    "app/services/ai/scanner/contract.py",
    "app/services/ai/scanner/image.py",
    "app/services/ai/scanner/prompts.py",
    "app/services/ai/scanner/service.py",
    "app/api/v1/ai.py",
    "app/main.py",
]

for source in sources:
    path = ROOT / source

    if not path.exists():
        raise RuntimeError(f"Required source missing: {source}")

    py_compile.compile(
        str(path),
        doraise=True,
    )

    print(f"{source}: PASS")

print("Source compilation: PASS")


# ============================================================================
# TASK 116 — PROMPT COMPATIBILITY
# ============================================================================
print()
print("===== TASK 116 — SCANNER PROMPT COMPATIBILITY =====")

sys.path.insert(0, str(ROOT))

from app.services.ai.scanner.prompts import (
    HERITAGE_SCANNER_SYSTEM_PROMPT,
    SCANNER_INTELLIGENCE_RULES,
)

if not HERITAGE_SCANNER_SYSTEM_PROMPT.strip():
    raise RuntimeError("HERITAGE_SCANNER_SYSTEM_PROMPT is empty.")

if not SCANNER_INTELLIGENCE_RULES.strip():
    raise RuntimeError("SCANNER_INTELLIGENCE_RULES is empty.")

print("HERITAGE_SCANNER_SYSTEM_PROMPT: PASS")
print("SCANNER_INTELLIGENCE_RULES: PASS")
print("Prompt compatibility: PASS")


# ============================================================================
# TASK 117 — CONTRACT + SERVICE IMPORT
# ============================================================================
print()
print("===== TASK 117 — SCANNER CONTRACT + SERVICE =====")

from app.services.ai.scanner.contract import (
    HeritageScannerResult,
    HeritageScannerResponse,
)

from app.services.ai.scanner.service import (
    HeritageScannerService,
)

print("HeritageScannerResult: PASS")
print("HeritageScannerResponse: PASS")
print("HeritageScannerService: PASS")


# ============================================================================
# TASK 118 — ORM + REPOSITORY + ROUTER
# ============================================================================
print()
print("===== TASK 118 — ORM + REPOSITORY + ROUTER =====")

from app.db.base import Base
from app.models.scan import Scan
from app.repositories.scan import ScanRepository
from app.api.v1.ai import router


required_tables = {
    "users",
    "scans",
    "heritage_sites",
    "heritage_site_historical_events",
    "heritage_site_media",
    "heritage_site_metadata",
    "heritage_site_relations",
    "heritage_site_sources",
    "ai_knowledge_documents",
    "ai_knowledge_chunks",
    "ai_embeddings",
}

registered = set(Base.metadata.tables.keys())
missing = required_tables - registered

if missing:
    raise RuntimeError(
        f"ORM registration missing tables: {sorted(missing)}"
    )

print(f"Registered ORM tables: {len(registered)}")
print("scans table: PASS")
print("ScanRepository: PASS")
print("AI router: PASS")

routes = {
    (tuple(sorted(route.methods)), route.path)
    for route in router.routes
}

required_routes = {
    (("POST",), "/ai/scan"),
    (("GET",), "/ai/scans"),
    (("GET",), "/ai/scans/{scan_id}"),
}

if not required_routes.issubset(routes):
    raise RuntimeError(
        f"Required scanner routes missing. Found: {routes}"
    )

print("Scanner routes: PASS")


# ============================================================================
# TASK 119 — DATABASE STATE
# ============================================================================
print()
print("===== TASK 119 — DATABASE SAFETY STATE =====")

from app.db.session import SessionLocal

db = SessionLocal()

try:
    existing_scans = db.query(Scan).count()
    print("Existing scans:", existing_scans)
finally:
    db.close()

print("Database connectivity: PASS")
print("No database mutation performed by validation: PASS")


# ============================================================================
# TASK 120 — SCANNER CONTRACT REGRESSION
# ============================================================================
print()
print("===== TASK 120 — SCANNER CONTRACT REGRESSION =====")

valid_result = HeritageScannerResult(
    identified_name="Controlled Heritage Site",
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    category="MONUMENT",
    location="Controlled Test Location",
    country="India",
    confidence=0.95,
    confidence_level="HIGH",
    description="Controlled validation result.",
    architectural_style="Historic",
    historical_period="Test Period",
    historical_significance="Controlled validation significance.",
    visual_evidence=[
        "Visible architectural structure"
    ],
    alternative_matches=[],
    grounding_status="GROUNDED",
)

response = HeritageScannerResponse(
    scan_id="00000000-0000-0000-0000-000000000000",
    result=valid_result,
)

assert response.result.identification_status == "IDENTIFIED"
assert response.result.confidence_level == "HIGH"

print("Valid scanner result: PASS")
print("Scanner response contract: PASS")


# ============================================================================
# TASK 121 — JSON BOUNDARY REGRESSION
# ============================================================================
print()
print("===== TASK 121 — JSON BOUNDARY REGRESSION =====")

import json

payload = json.loads(
    valid_result.model_dump_json()
)

assert payload["identification_status"] == "IDENTIFIED"
assert "visual_evidence" in payload
assert "confidence" in payload

print("Scanner JSON serialization: PASS")
print("Scanner JSON boundary: PASS")


# ============================================================================
# TASK 122 — PERSISTENCE MAPPING REGRESSION
# ============================================================================
print()
print("===== TASK 122 — PERSISTENCE MAPPING REGRESSION =====")

repository_source = (
    ROOT / "app/repositories/scan.py"
).read_text(encoding="utf-8")

required_mapping = [
    "identification_status=result.identification_status",
    "evidence_quality=result.evidence_quality",
    "identified_name=result.identified_name",
    "category=result.category",
    "location=result.location",
    "country=result.country",
    "confidence=result.confidence",
    "confidence_level=result.confidence_level",
    "description=result.description",
    "architectural_style=result.architectural_style",
    "historical_period=result.historical_period",
    "historical_significance=result.historical_significance",
    "visual_evidence=result.visual_evidence",
    "alternative_matches=result.alternative_matches",
    "grounding_status=result.grounding_status",
]

for marker in required_mapping:
    if marker not in repository_source:
        raise RuntimeError(
            f"Persistence mapping missing: {marker}"
        )

print("Scanner result → Scan mapping: PASS")


# ============================================================================
# TASK 123 — PERSISTENCE SAFETY
# ============================================================================
print()
print("===== TASK 123 — PERSISTENCE SAFETY =====")

forbidden = [
    "image_bytes",
    "image_base64",
    "GEMINI_API_KEY",
    "access_token",
    "refresh_token",
    "raw_response",
    "response.text",
]

for marker in forbidden:
    if marker in repository_source:
        raise RuntimeError(
            f"Forbidden persistence marker found: {marker}"
        )

scan_source = (
    ROOT / "app/models/scan.py"
).read_text(encoding="utf-8")

for marker in [
    "image_bytes",
    "image_base64",
    "raw_response",
]:
    if marker in scan_source:
        raise RuntimeError(
            f"Forbidden Scan persistence marker found: {marker}"
        )

print("Raw image persistence: NOT PRESENT")
print("Base64 persistence: NOT PRESENT")
print("Raw Gemini response persistence: NOT PRESENT")
print("Persistence safety: PASS")


# ============================================================================
# TASK 124 — FINAL APPLICATION GATE
# ============================================================================
print()
print("===== TASK 124 — FINAL APPLICATION GATE =====")

from app.main import app

print("FastAPI application import: PASS")
print("Application routes:", len(app.routes))
print("Scanner architecture: PASS")
print("Scanner prompt compatibility: PASS")
print("Scanner contract: PASS")
print("ORM registration: PASS")
print("Repository: PASS")
print("Persistence safety: PASS")

print()
print("=" * 80)
print("TASKS 115-124 COMPLETE")
print("=" * 80)
print("Prompt compatibility: PASS")
print("Source compilation: PASS")
print("Scanner contract: PASS")
print("Service import: PASS")
print("ORM registration: PASS")
print("Repository architecture: PASS")
print("Database connectivity: PASS")
print("JSON boundary: PASS")
print("Persistence mapping: PASS")
print("Persistence safety: PASS")
print("Final application gate: PASS")
print()
print("REAL GEMINI REQUEST: NOT EXECUTED BY THIS BATCH")
print("DATABASE MUTATION: NONE")
print("QDRANT CHANGES: NONE")
print("EMBEDDINGS CREATED: NONE")
print()
print("READY FOR NEXT REAL RUNTIME VALIDATION BATCH")
print("=" * 80)

