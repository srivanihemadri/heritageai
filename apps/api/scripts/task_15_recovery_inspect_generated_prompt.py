from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)

print("=" * 80)
print("STEP 8C-003 — TASK 15-RECOVERY — INSPECT GENERATED SCANNER PROMPT")
print("=" * 80)

print()
print("===== 1. BUILD PROMPT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str):
    raise RuntimeError("Generated scanner prompt is not a string.")

print("Prompt type:", type(prompt).__name__)
print("Prompt length:", len(prompt))
print("Prompt construction: PASS")

print()
print("===== 2. PRINT INTELLIGENCE RULES =====")

print(SCANNER_INTELLIGENCE_RULES)

print()
print("===== 3. PRINT GENERATED PROMPT =====")

print(prompt)

print()
print("===== 4. CHECK PRODUCTION INTELLIGENCE TERMS =====")

terms = [
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
]

for term in terms:
    present = term.lower() in prompt.lower()
    print(
        f"{term}:",
        "PRESENT" if present else "MISSING",
    )

print()
print("===== 5. CHECK CONSTANT INTEGRATION =====")

if SCANNER_INTELLIGENCE_RULES.strip() in prompt:
    print("SCANNER_INTELLIGENCE_RULES embedded directly: PASS")
else:
    print(
        "SCANNER_INTELLIGENCE_RULES embedded directly: NOT CONFIRMED"
    )

print()
print("===== 6. SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 15-RECOVERY COMPLETE")
print("=" * 80)

print("Generated prompt inspection: COMPLETE")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
