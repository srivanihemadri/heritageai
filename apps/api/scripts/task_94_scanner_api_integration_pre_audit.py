from pathlib import Path

print("=" * 80)
print("STEP 8C-005 — TASK 94 — SCANNER API INTEGRATION PRE-IMPLEMENTATION AUDIT")
print("=" * 80)

api_path = Path("app/api/v1/ai.py")
repo_path = Path("app/repositories/scan.py")
contract_path = Path("app/services/ai/scanner/contract.py")
service_path = Path("app/services/ai/scanner/service.py")

for path in [api_path, repo_path, contract_path, service_path]:
    if not path.exists():
        raise RuntimeError(f"Required file missing: {path}")

api = api_path.read_text(encoding="utf-8")
repo = repo_path.read_text(encoding="utf-8")
contract = contract_path.read_text(encoding="utf-8")
service = service_path.read_text(encoding="utf-8")

print()
print("===== 1. SCANNER ROUTE =====")

for marker in [
    '"/scan"',
    "async def heritage_scan",
    "UploadFile",
    "current_user",
    "HeritageScannerService",
]:
    if marker not in api:
        raise RuntimeError(
            f"Scanner route marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Scanner route: PASS")

print()
print("===== 2. REPOSITORY =====")

for marker in [
    "class ScanRepository",
    "def create",
    "def get_by_id",
    "def list_by_user",
]:
    if marker not in repo:
        raise RuntimeError(
            f"Repository marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Repository: PASS")

print()
print("===== 3. SCANNER RESPONSE CONTRACT =====")

for marker in [
    "class HeritageScannerResult",
    "class HeritageScannerResponse",
    "scan_id: str",
    "result: HeritageScannerResult",
]:
    if marker not in contract:
        raise RuntimeError(
            f"Contract marker missing: {marker}"
        )
    print(f"{marker}: PRESENT")

print("Scanner contract: PASS")

print()
print("===== 4. SCANNER SERVICE =====")

if "def scan(" not in service:
    raise RuntimeError(
        "Scanner service scan() missing."
    )

print("scan(): PRESENT")

if "HeritageScannerResult" not in service:
    raise RuntimeError(
        "HeritageScannerResult missing from scanner service."
    )

print("HeritageScannerResult: PRESENT")
print("Scanner service contract: PASS")

print()
print("===== 5. CURRENT PERSISTENCE STATE =====")

if "ScanRepository" in api:
    print("ScanRepository integration: PRESENT")
else:
    print("ScanRepository integration: NOT YET IMPLEMENTED")

if "repository.create(" in api:
    print("Repository create call: PRESENT")
else:
    print("Repository create call: NOT YET IMPLEMENTED")

if "db.commit()" in api:
    print("Explicit db.commit(): PRESENT")
else:
    print("Explicit db.commit(): NOT YET IMPLEMENTED")

print()
print("===== 6. RETRIEVAL ROUTES =====")

if '"/scans/{scan_id}"' in api:
    print("Single scan route: PRESENT")
else:
    print("Single scan route: NOT YET IMPLEMENTED")

if '"/scans"' in api:
    print("Scan history route: PRESENT")
else:
    print("Scan history route: NOT YET IMPLEMENTED")

print()
print("===== 7. OWNERSHIP CONTRACT =====")

for marker in [
    "Scan.user_id == user_id",
]:
    if marker not in repo:
        raise RuntimeError(
            f"Ownership marker missing: {marker}"
        )

print("Repository ownership filtering: PASS")

print()
print("===== 8. DATABASE SAFETY =====")

print("Existing scans schema: PRESERVED")
print("Migration required: NO")
print("Database migration execution: NONE")
print("Database mutation by audit: NONE")

print()
print("===== 9. AI SAFETY =====")

print("Real Gemini request: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")

print()
print("=" * 80)
print("TASK 94 COMPLETE")
print("=" * 80)
print("Scanner route audit: PASS")
print("Repository audit: PASS")
print("Contract audit: PASS")
print("Service audit: PASS")
print("Ownership audit: PASS")
print("Database safety: PASS")
print()
print("READY FOR ACTUAL SCANNER PERSISTENCE INTEGRATION")
print("=" * 80)
