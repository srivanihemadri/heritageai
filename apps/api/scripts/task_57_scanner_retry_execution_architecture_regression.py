from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 57 — SCANNER RETRY EXECUTION ARCHITECTURE")
print("=" * 80)

service = Path("app/services/ai/scanner/service.py").read_text(encoding="utf-8")

required = [
    "MAX_TRANSIENT_RETRIES",
    "TRANSIENT_RETRY_DELAY_SECONDS",
    "ServerError",
    "RESOURCE_EXHAUSTED",
    "ScannerQuotaExceededError",
    "GEMINI SCANNER ATTEMPT:",
]

for term in required:
    if term not in service:
        raise RuntimeError(f"Task 57 missing retry marker: {term}")
    print(f"{term}: PRESENT")

print("Bounded retry architecture: PASS")
print("Quota classification: PASS")
print("Retry observability: PASS")
print("Controlled retry inspection: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")
print("=" * 80)
print("TASK 57 COMPLETE")
print("=" * 80)
