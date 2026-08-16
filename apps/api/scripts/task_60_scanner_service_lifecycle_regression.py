from pathlib import Path

print("=" * 80)
print("STEP 8C-003 — TASK 60 — SCANNER SERVICE LIFECYCLE REGRESSION")
print("=" * 80)

service_path = Path("app/services/ai/scanner/service.py")
router_path = Path("app/api/v1/ai.py")

service = service_path.read_text(encoding="utf-8")
router = router_path.read_text(encoding="utf-8")

if "class HeritageScannerService" not in service:
    raise RuntimeError("HeritageScannerService missing.")

if "finally:" not in router:
    raise RuntimeError("Scanner router cleanup boundary missing.")

if "close" not in router:
    raise RuntimeError("Scanner client cleanup marker missing.")

print("HeritageScannerService: PRESENT")
print("Router finally boundary: PRESENT")
print("Client cleanup boundary: PRESENT")
print("Scanner lifecycle architecture: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")
print("=" * 80)
print("TASK 60 COMPLETE")
print("=" * 80)
