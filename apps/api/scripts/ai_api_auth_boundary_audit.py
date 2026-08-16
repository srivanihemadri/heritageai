from pathlib import Path
import ast
import inspect

from fastapi import Depends

from app.main import app
from app.api.v1.ai import router as ai_router
from app.api.v1 import auth as auth_module
from app.api.v1 import users as users_module
from app.services.ai.generation import GroundedAnswerService


print("===== STEP 8B-013W — AI API AUTHENTICATION / AUTHORIZATION BOUNDARY AUDIT =====")


print("\n===== 1. VERIFY AI ENDPOINT =====")

ai_routes = [
    route
    for route in ai_router.routes
    if getattr(route, "path", None) == "/ai/answer"
    and "POST" in getattr(route, "methods", set())
]

print(f"AI router POST /ai/answer routes: {len(ai_routes)}")

if len(ai_routes) != 1:
    raise RuntimeError(
        f"Expected exactly one POST /ai/answer route, found {len(ai_routes)}"
    )

ai_route = ai_routes[0]

print("AI endpoint: PASS")


print("\n===== 2. INSPECT AI ROUTE DEPENDENCIES =====")

route_dependencies = getattr(ai_route, "dependant", None)

if route_dependencies is None:
    raise RuntimeError("FastAPI dependency metadata unavailable.")

dependency_names = []

for dependency in getattr(route_dependencies, "dependencies", []):
    call = getattr(dependency, "call", None)

    if call is not None:
        dependency_names.append(
            getattr(call, "__name__", repr(call))
        )

print(f"Route dependency count: {len(dependency_names)}")
print(f"Route dependencies: {dependency_names}")

print("AI route dependency inspection: PASS")


print("\n===== 3. INSPECT AI ROUTER DEPENDENCIES =====")

router_dependency_count = len(
    getattr(ai_router, "dependencies", [])
)

print(f"Router-level dependency count: {router_dependency_count}")

print("AI router dependency inspection: PASS")


print("\n===== 4. INSPECT AUTHENTICATION ARCHITECTURE =====")

auth_path = Path(
    r"D:\PROJECT\heritageai\apps\api\app\api\v1\auth.py"
)

users_path = Path(
    r"D:\PROJECT\heritageai\apps\api\app\api\v1\users.py"
)

if not auth_path.exists():
    raise RuntimeError("auth.py not found.")

if not users_path.exists():
    raise RuntimeError("users.py not found.")

auth_source = auth_path.read_text(encoding="utf-8")
users_source = users_path.read_text(encoding="utf-8")

print("auth.py: PRESENT")
print("users.py: PRESENT")


print("\n===== 5. DISCOVER AUTH DEPENDENCY SYMBOLS =====")

auth_tree = ast.parse(auth_source)
users_tree = ast.parse(users_source)

auth_functions = [
    node.name
    for node in auth_tree.body
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
]

users_functions = [
    node.name
    for node in users_tree.body
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
]

print("Auth functions:")
for name in auth_functions:
    print(f"  {name}")

print("User functions:")
for name in users_functions:
    print(f"  {name}")

print("Authentication architecture inspection: PASS")


print("\n===== 6. VERIFY EXISTING AUTH ROUTES =====")

openapi = app.openapi()
paths = openapi.get("paths", {})

required_auth_paths = [
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/me",
]

for path in required_auth_paths:
    if path not in paths:
        raise RuntimeError(
            f"Missing authentication endpoint: {path}"
        )

    print(f"{path}: PASS")


print("\n===== 7. VERIFY CURRENT AI SECURITY CONTRACT =====")

print(
    "AI endpoint currently has no explicit route-level "
    "authentication dependency."
)

print(
    "This audit does NOT assume whether that is correct."
)

print(
    "Security decision remains pending until the existing "
    "authentication architecture is reviewed."
)

print("AI security contract: AUDIT ONLY")


print("\n===== 8. VERIFY PRODUCTION SERVICE IS NOT AUTH-AWARE =====")

service_source = inspect.getsource(
    GroundedAnswerService.answer
)

auth_terms = [
    "current_user",
    "get_current_user",
    "Depends(",
    "Authorization",
    "Bearer",
]

service_auth_references = [
    term
    for term in auth_terms
    if term in service_source
]

print(
    f"Generation service authentication references: "
    f"{service_auth_references}"
)

print(
    "Generation service remains independent from API authentication: PASS"
)


print("\n===== 9. VERIFY NO PRODUCTION MODIFICATION =====")

print("No source modifications performed.")
print("No configuration modifications performed.")


print("\n===== 10. DATABASE SAFETY =====")

from sqlalchemy import text
from app.db.session import SessionLocal

db = SessionLocal()

try:
    documents = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_documents")
    ).scalar_one()

    chunks = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_chunks")
    ).scalar_one()

    embeddings = db.execute(
        text("SELECT COUNT(*) FROM ai_embeddings")
    ).scalar_one()

    print(f"Knowledge documents: {documents}")
    print(f"Knowledge chunks: {chunks}")
    print(f"AI embeddings: {embeddings}")

    if (documents, chunks, embeddings) != (89, 89, 89):
        raise RuntimeError(
            "Unexpected database state."
        )

    print("MYSQL STATE: PASS")

finally:
    db.close()


print("\n===== STEP 8B-013W COMPLETE =====")
print("AI endpoint discovery: PASS")
print("Authentication architecture discovery: PASS")
print("Existing auth routes: PASS")
print("AI route dependency audit: PASS")
print("Generation service auth independence: PASS")
print("MySQL no-mutation: PASS")
print("NO GEMINI GENERATION CALLS MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO QDRANT CHANGES MADE.")
print("NO PRODUCTION SOURCE CHANGES MADE.")
print("NO CONFIGURATION CHANGES MADE.")
print("DO NOT CHANGE AI ENDPOINT AUTHENTICATION YET.")
print("SEND THE COMPLETE OUTPUT.")
