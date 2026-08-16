from __future__ import annotations

import inspect
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print(
    "STEP 8C-003 — TASK 15-RECOVERY-4 — "
    "INSPECT SCANNER RESPONSE PARSER"
)
print("=" * 80)


print()
print("===== 1. VERIFY SCANNER SERVICE =====")

print(
    "HeritageScannerService:",
    HeritageScannerService,
)

print("Service import: PASS")


print()
print("===== 2. INSPECT SERVICE METHODS =====")

methods = [
    name
    for name, value in inspect.getmembers(
        HeritageScannerService,
        predicate=inspect.isfunction,
    )
]

for name in methods:
    print(
        "METHOD:",
        name,
    )

print("Method discovery: PASS")


print()
print("===== 3. IDENTIFY RESPONSE PARSING METHODS =====")

parser_candidates = []

for name in methods:

    lowered = name.lower()

    if any(
        keyword in lowered
        for keyword in [
            "parse",
            "response",
            "result",
            "payload",
        ]
    ):
        parser_candidates.append(name)

if not parser_candidates:
    print(
        "No parser-named method found."
    )
else:
    for name in parser_candidates:
        print(
            "PARSER CANDIDATE:",
            name,
        )

print("Parser candidate discovery: COMPLETE")


print()
print("===== 4. PRINT CANDIDATE SOURCE =====")

for name in parser_candidates:

    method = getattr(
        HeritageScannerService,
        name,
    )

    print()
    print(
        f"----- {name} -----"
    )
    print(
        inspect.getsource(method)
    )

print()
print("Candidate source inspection: PASS")


print()
print("===== 5. INSPECT FULL SCAN METHOD =====")

scan_method = getattr(
    HeritageScannerService,
    "scan",
    None,
)

if scan_method is None:
    raise RuntimeError(
        "HeritageScannerService.scan not found."
    )

scan_source = inspect.getsource(
    scan_method
)

print(
    scan_source
)

print("Scan method inspection: PASS")


print()
print("===== 6. CHECK RESPONSE FIELD REFERENCES =====")

fields = [
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
    "identification_status",
    "evidence_quality",
]

combined_source = "\n".join(
    [
        inspect.getsource(
            getattr(HeritageScannerService, name)
        )
        for name in methods
    ]
)

for field in fields:

    print(
        f"{field}:",
        "PRESENT"
        if field in combined_source
        else "NOT FOUND",
    )


print()
print("===== 7. SAFETY =====")

print("Read-only inspection: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 15-RECOVERY-4 COMPLETE")
print("=" * 80)

print("Scanner parser inspection: COMPLETE")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
