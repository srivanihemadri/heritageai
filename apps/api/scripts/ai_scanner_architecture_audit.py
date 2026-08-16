"""
HeritageAI — AI Scanner Architecture Audit
STEP 8C-001
READ-ONLY AUDIT — NO PRODUCTION MODIFICATIONS
"""

from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"


def banner(text):
    print()
    print("=" * 80)
    print(text)
    print("=" * 80)


def exists(relative):
    path = APP / relative
    status = path.exists()
    print(f"{relative}: {'PRESENT' if status else 'MISSING'}")
    return status


def inspect_python(relative):
    path = APP / relative
    if not path.exists():
        print(f"{relative}: MISSING")
        return

    try:
        ast.parse(path.read_text(encoding="utf-8"))
        print(f"{relative}: SYNTAX PASS")
    except Exception as exc:
        print(f"{relative}: SYNTAX FAIL — {exc}")


banner("STEP 8C-001 — AI HERITAGE SCANNER ARCHITECTURE AUDIT")

print(f"Project root: {ROOT}")
print(f"Application root: {APP}")

banner("1. EXISTING AI ARCHITECTURE")

ai_root = APP / "services" / "ai"

if ai_root.exists():
    for path in sorted(ai_root.rglob("*.py")):
        print(path.relative_to(ROOT))
else:
    print("AI service directory: MISSING")

banner("2. AI ROUTER")

inspect_python("api/v1/ai.py")

banner("3. AI GENERATION SERVICE")

inspect_python("services/ai/generation/service.py")

banner("4. AI RETRIEVAL SERVICES")

for candidate in [
    "services/ai/retrieval/service.py",
    "services/ai/retrieval/relevance_gate.py",
]:
    inspect_python(candidate)

banner("5. AUTHENTICATION ARCHITECTURE")

for candidate in [
    "dependencies.py",
    "security.py",
    "api/v1/auth.py",
]:
    inspect_python(candidate)

banner("6. MEDIA / FILE ARCHITECTURE")

media_candidates = [
    "api/v1/heritage_sites.py",
    "services/media",
    "core/config.py",
]

for candidate in media_candidates:
    path = APP / candidate
    print(
        f"{candidate}: "
        f"{'PRESENT' if path.exists() else 'MISSING'}"
    )

banner("7. GEMINI REFERENCES")

matches = []

for path in APP.rglob("*.py"):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    lowered = text.lower()

    if "gemini" in lowered:
        matches.append(path.relative_to(ROOT))

for path in sorted(set(matches)):
    print(path)

banner("8. IMAGE / UPLOAD REFERENCES")

image_terms = (
    "upload",
    "image",
    "media",
    "multipart",
    "uploadfile",
    "file",
)

for path in APP.rglob("*.py"):
    try:
        text = path.read_text(encoding="utf-8").lower()
    except Exception:
        continue

    if any(term in text for term in image_terms):
        print(path.relative_to(ROOT))

banner("9. SCHEMA / MODEL DISCOVERY")

schema_root = APP / "schemas"

if schema_root.exists():
    for path in sorted(schema_root.rglob("*.py")):
        print(path.relative_to(ROOT))
else:
    print("Schema directory: MISSING")

banner("10. DATABASE / KNOWLEDGE ARCHITECTURE")

for root_name in ["models", "repositories", "db", "database"]:
    path = APP / root_name

    if path.exists():
        print(f"{root_name}: PRESENT")
        for child in sorted(path.rglob("*.py")):
            print(f"  {child.relative_to(ROOT)}")

banner("11. EXISTING API ROUTES")

try:
    sys.path.insert(0, str(ROOT))

    from app.main import app

    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)

        if path:
            print(f"{sorted(methods or [])} {path}")

    print("FastAPI application import: PASS")

except Exception as exc:
    print(f"FastAPI application import: FAIL — {exc}")

banner("12. PRODUCTION SAFETY")

print("NO PRODUCTION SOURCE CHANGES MADE.")
print("NO CONFIGURATION CHANGES MADE.")
print("NO GEMINI GENERATION CALLS MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO QDRANT CHANGES MADE.")
print("NO EMBEDDINGS CREATED.")

banner("STEP 8C-001 COMPLETE")
print("Scanner architecture audit: COMPLETE")
print("DO NOT IMPLEMENT THE SCANNER YET.")
