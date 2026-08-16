from __future__ import annotations

import inspect
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.services.ai.scanner import prompts


print("=" * 80)
print(
    "STEP 8C-003 — TASK 15-RECOVERY-2 — "
    "INSPECT SCANNER PROMPT BUILDER"
)
print("=" * 80)


print()
print("===== 1. VERIFY PROMPT MODULE =====")

print(
    "Prompt module:",
    prompts.__file__,
)

print("Prompt module import: PASS")


print()
print("===== 2. INSPECT BUILD_SCANNER_PROMPT =====")

builder = prompts.build_scanner_prompt

source = inspect.getsource(builder)

print("build_scanner_prompt source:")
print("-" * 80)
print(source)
print("-" * 80)

print("Builder source inspection: PASS")


print()
print("===== 3. VERIFY INTELLIGENCE CONSTANT =====")

rules = prompts.SCANNER_INTELLIGENCE_RULES

print(
    "SCANNER_INTELLIGENCE_RULES length:",
    len(rules),
)

required_rules = [
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

for rule in required_rules:

    print(
        f"{rule}:",
        "PRESENT" if rule.lower() in rules.lower() else "MISSING",
    )


print()
print("===== 4. INSPECT GENERATED PROMPT =====")

generated = builder()

print(
    "Generated prompt length:",
    len(generated),
)

print()
print(generated)


print()
print("===== 5. COMPARE RULE INTEGRATION =====")

if rules.strip() in generated:

    print(
        "SCANNER_INTELLIGENCE_RULES direct integration: PASS"
    )

else:

    print(
        "SCANNER_INTELLIGENCE_RULES direct integration: MISSING"
    )


print()
print("===== 6. CHECK NEW RESPONSE FIELDS =====")

for field in [
    "identification_status",
    "evidence_quality",
]:

    print(
        f"{field}:",
        "PRESENT" if field in generated else "MISSING",
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
print("STEP 8C-003 — TASK 15-RECOVERY-2 COMPLETE")
print("=" * 80)

print("Prompt builder inspection: COMPLETE")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
