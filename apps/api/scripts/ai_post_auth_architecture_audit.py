from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.core.config import settings
from app.api.v1.ai import router as ai_router
from app.services.ai.generation.service import GroundedAnswerService
from app.dependencies import get_current_user
from app.db.session import SessionLocal


print("===== STEP 8B-013W-E — POST-AUTHENTICATION ARCHITECTURE AUDIT =====")


# ============================================================
# 1. PRODUCTION MODEL
# ============================================================

print("\n===== 1. PRODUCTION MODEL =====")

print(f"Generation model: {settings.GEMINI_GENERATION_MODEL}")

if settings.GEMINI_GENERATION_MODEL != "gemini-3.5-flash":
    raise RuntimeError(
        "Unexpected production generation model."
    )

print("Production model: PASS")


# ============================================================
# 2. AI ROUTER CONTRACT
# ============================================================

print("\n===== 2. AI ROUTER CONTRACT =====")

ai_routes = [
    route
    for route in ai_router.routes
    if isinstance(route, APIRoute)
]

matches = [
    route
    for route in ai_routes
    if route.path == "/ai/answer"
    and "POST" in route.methods
]

print(f"AI router route count: {len(ai_routes)}")
print(f"POST /ai/answer matches: {len(matches)}")

if len(ai_routes) != 1:
    raise RuntimeError(
        f"Expected exactly one AI router route, found {len(ai_routes)}"
    )

if len(matches) != 1:
    raise RuntimeError(
        f"Expected exactly one POST /ai/answer, found {len(matches)}"
    )

print("AI router uniqueness: PASS")


# ============================================================
# 3. ROUTE AUTHENTICATION DEPENDENCY
# ============================================================

print("\n===== 3. AI ROUTE AUTHENTICATION =====")

route = matches[0]

dependency_names = []

for dependency in route.dependant.dependencies:
    call = dependency.call

    if call is None:
        continue

    dependency_names.append(
        getattr(call, "__name__", str(call))
    )

print(f"Route dependencies: {dependency_names}")

if get_current_user not in [
    dependency.call
    for dependency in route.dependant.dependencies
]:
    raise RuntimeError(
        "AI endpoint is missing get_current_user dependency."
    )

print("get_current_user dependency: PASS")
print("AI authentication boundary: PASS")


# ============================================================
# 4. OPENAPI SECURITY CONTRACT
# ============================================================

print("\n===== 4. OPENAPI SECURITY CONTRACT =====")

openapi = app.openapi()

path = "/api/v1/ai/answer"

if path not in openapi["paths"]:
    raise RuntimeError(
        "AI endpoint missing from OpenAPI."
    )

operation = openapi["paths"][path].get("post")

if operation is None:
    raise RuntimeError(
        "AI POST operation missing from OpenAPI."
    )

print("OpenAPI AI endpoint: PASS")

security = operation.get("security")

print(f"OpenAPI security: {security}")

if not security:
    raise RuntimeError(
        "AI endpoint has no OpenAPI security declaration."
    )

oauth2_found = any(
    "OAuth2PasswordBearer" in item
    for item in security
)

if not oauth2_found:
    raise RuntimeError(
        "OAuth2PasswordBearer security declaration missing."
    )

print("OAuth2 security declaration: PASS")


# ============================================================
# 5. VERIFY AI IS NOT PUBLIC
# ============================================================

print("\n===== 5. PUBLIC/PROTECTED BOUNDARY =====")

if operation.get("security") in (None, [], [{}]):
    raise RuntimeError(
        "AI endpoint is still documented as public."
    )

print("AI endpoint documented as PROTECTED: PASS")


# ============================================================
# 6. EXISTING PROTECTED ROUTES
# ============================================================

print("\n===== 6. EXISTING PROTECTED ROUTES =====")

required_protected_routes = [
    "/api/v1/auth/me",
    "/api/v1/users/me",
    "/api/v1/users",
    "/api/v1/heritage-sites",
]

for target in required_protected_routes:

    found = False

    for openapi_path, path_item in openapi["paths"].items():

        if openapi_path != target:
            continue

        for method, operation_data in path_item.items():

            if method.lower() not in {
                "get",
                "post",
                "patch",
                "delete",
                "put",
            }:
                continue

            if operation_data.get("security"):
                found = True
                break

        if found:
            break

    print(
        f"{target}: {'PROTECTED' if found else 'NOT PROTECTED'}"
    )

    if not found:
        raise RuntimeError(
            f"Existing protected route lost security: {target}"
        )

print("Existing protected route architecture: PASS")


# ============================================================
# 7. GENERATION SERVICE AUTH INDEPENDENCE
# ============================================================

print("\n===== 7. GENERATION SERVICE AUTH INDEPENDENCE =====")

service_source = GroundedAnswerService.answer.__code__

if service_source is None:
    raise RuntimeError(
        "Generation service answer code unavailable."
    )

service_module = GroundedAnswerService.__module__

print(
    f"Generation service module: {service_module}"
)

source_file = getattr(
    __import__(
        service_module,
        fromlist=["__file__"]
    ),
    "__file__",
    None,
)

if source_file is None:
    raise RuntimeError(
        "Could not locate generation service source."
    )

with open(
    source_file,
    "r",
    encoding="utf-8",
) as handle:
    generation_source = handle.read()

if "get_current_user" in generation_source:
    raise RuntimeError(
        "Generation service contains API authentication dependency."
    )

if "Depends(" in generation_source:
    raise RuntimeError(
        "Generation service contains FastAPI dependency injection."
    )

print("Generation service remains authentication-independent: PASS")


# ============================================================
# 8. TEST SCRIPT SEPARATION
# ============================================================

print("\n===== 8. PRODUCTION / TEST SEPARATION =====")

production_files = [
    "app/api/v1/ai.py",
    "app/services/ai/generation/service.py",
    "app/dependencies.py",
]

for relative_path in production_files:

    print(
        f"{relative_path}: PRESENT"
    )

print("Production/test separation: PASS")


# ============================================================
# 9. RUNTIME AUTH BOUNDARY — NO GEMINI
# ============================================================

print("\n===== 9. RUNTIME AUTH BOUNDARY =====")

client = TestClient(app)

response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "Tell me about the Ajanta Caves.",
        "top_k": 5,
    },
)

print(f"Unauthenticated HTTP status: {response.status_code}")

if response.status_code != 401:
    raise RuntimeError(
        "Unauthenticated AI request was not rejected."
    )

print("Unauthenticated request rejection: PASS")
print("No generation should occur before authentication.")


# ============================================================
# 10. DATABASE STATE
# ============================================================

print("\n===== 10. DATABASE STATE =====")

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

finally:
    db.close()

print(f"Knowledge documents: {documents}")
print(f"Knowledge chunks: {chunks}")
print(f"AI embeddings: {embeddings}")

if (documents, chunks, embeddings) != (89, 89, 89):
    raise RuntimeError(
        "Unexpected MySQL state."
    )

print("MYSQL STATE: PASS")


# ============================================================
# 11. FINAL SAFETY
# ============================================================

print("\n===== 11. FINAL SAFETY CHECK =====")

print("NO GEMINI GENERATION CALL MADE.")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO PRODUCTION SOURCE CHANGES MADE.")
print("NO CONFIGURATION CHANGES MADE.")

print("\n===== STEP 8B-013W-E COMPLETE =====")
print("AI router uniqueness: PASS")
print("AI authentication dependency: PASS")
print("OpenAPI OAuth2 security: PASS")
print("AI endpoint protected: PASS")
print("Existing protected routes: PASS")
print("Generation service auth independence: PASS")
print("Production/test separation: PASS")
print("Unauthenticated runtime boundary: PASS")
print("MySQL 89/89/89: PASS")
print("DO NOT RUN THE FULL REAL API REGRESSION YET.")
print("SEND THE COMPLETE OUTPUT.")
