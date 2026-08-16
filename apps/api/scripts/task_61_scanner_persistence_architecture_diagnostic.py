from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 61 — SCANNER PERSISTENCE ARCHITECTURE DIAGNOSTIC")
print("=" * 80)

root = Path("app")

matches = []
for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if any(term in text.lower() for term in [
        "scanner",
        "scan_id",
        "scan history",
        "scan_history",
    ]):
        matches.append(path)

print(f"Scanner-related Python files discovered: {len(matches)}")

for path in matches:
    print(f"PRESENT: {path.as_posix()}")

print("Persistence architecture discovery: COMPLETE")
print("This task does not mutate persistence.")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
print("TASK 61 COMPLETE")
print("=" * 80)
