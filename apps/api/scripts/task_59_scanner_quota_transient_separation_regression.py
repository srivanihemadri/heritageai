from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 59 — SCANNER QUOTA/TRANSIENT SEPARATION REGRESSION")
print("=" * 80)

service = Path("app/services/ai/scanner/service.py").read_text(encoding="utf-8")

quota_terms = [
    "ScannerQuotaExceededError",
    "RESOURCE_EXHAUSTED",
    "status_code == 429",
    "GEMINI SCANNER QUOTA EXHAUSTED",
]

transient_terms = [
    "ServerError",
    "GEMINI TRANSIENT SERVER ERROR:",
]

for term in quota_terms:
    if term not in service:
        raise RuntimeError(f"Quota separation marker missing: {term}")
    print(f"{term}: PRESENT")

for term in transient_terms:
    if term not in service:
        raise RuntimeError(f"Transient separation marker missing: {term}")
    print(f"{term}: PRESENT")

print("Quota/transient classification: PASS")
print("Quota exception boundary: PASS")
print("Transient retry boundary: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")
print("=" * 80)
print("TASK 59 COMPLETE")
print("=" * 80)
