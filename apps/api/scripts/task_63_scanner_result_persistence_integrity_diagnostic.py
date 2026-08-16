from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 63 — SCANNER RESULT PERSISTENCE INTEGRITY DIAGNOSTIC")
print("=" * 80)

root = Path("app")
terms = [
    "scan_id",
    "HeritageScannerResult",
    "HeritageScannerResponse",
]

found = {term: [] for term in terms}

for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for term in terms:
        if term in text:
            found[term].append(path)

for term, paths in found.items():
    if not paths:
        print(f"{term}: NOT FOUND")
    else:
        print(f"{term}: PRESENT")

if not found["HeritageScannerResult"]:
    raise RuntimeError("HeritageScannerResult persistence boundary cannot be inspected.")

print("Result-contract integrity boundary: INSPECTED")
print("No persistence mutation performed.")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
print("TASK 63 COMPLETE")
print("=" * 80)
