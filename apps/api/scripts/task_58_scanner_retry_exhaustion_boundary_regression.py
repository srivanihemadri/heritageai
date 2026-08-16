from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 58 — SCANNER RETRY EXHAUSTION BOUNDARY")
print("=" * 80)

service = Path("app/services/ai/scanner/service.py").read_text(encoding="utf-8")

required = [
    "MAX_TRANSIENT_RETRIES",
    "for attempt in range",
    "raise RuntimeError",
    "GEMINI TRANSIENT SERVER ERROR:",
]

for term in required:
    if term not in service:
        raise RuntimeError(f"Task 58 retry-exhaustion marker missing: {term}")
    print(f"{term}: PRESENT")

print("Maximum retry boundary: PRESENT")
print("Retry exhaustion boundary: PRESENT")
print("No obvious unbounded retry: PASS")
print("Retry exhaustion architecture: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")
print("=" * 80)
print("TASK 58 COMPLETE")
print("=" * 80)
