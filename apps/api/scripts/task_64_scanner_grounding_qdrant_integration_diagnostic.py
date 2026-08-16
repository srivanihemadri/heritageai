from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 64 — SCANNER GROUNDING/QDRANT INTEGRATION DIAGNOSTIC")
print("=" * 80)

root = Path("app")
terms = [
    "qdrant",
    "grounding",
    "embedding",
    "retrieval",
]

found = {term: [] for term in terms}

for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    for term in terms:
        if term in text:
            found[term].append(path)

for term, paths in found.items():
    print(f"{term}: {'PRESENT' if paths else 'NOT FOUND'}")

print("Grounding integration architecture: INSPECTED")
print("Qdrant mutation: NONE")
print("Embedding creation: NONE")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
print("TASK 64 COMPLETE")
print("=" * 80)
