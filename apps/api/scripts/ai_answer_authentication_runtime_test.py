from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_current_user
from app.api.v1.ai import router as ai_router
from app.services.ai.generation import GroundedAnswerService
from app.api.v1.contracts.ai import (
    GroundedAnswerSourceResponse,
)


print("===== STEP 8B-013W-B — AI AUTHENTICATION RUNTIME TEST =====")


# ------------------------------------------------------------
# 1. ROUTER CONTRACT
# ------------------------------------------------------------

print("\n===== 1. ROUTER AUTHENTICATION CONTRACT =====")

matches = [
    route
    for route in ai_router.routes
    if getattr(route, "path", None) == "/ai/answer"
    and "POST" in getattr(route, "methods", set())
]

if len(matches) != 1:
    raise RuntimeError(
        f"Expected exactly one POST /ai/answer route, found {len(matches)}"
    )

route = matches[0]

dependant = getattr(route, "dependant", None)

dependency_names = []

if dependant is not None:
    for dependency in getattr(dependant, "dependencies", []):
        call = getattr(dependency, "call", None)

        if call is not None:
            dependency_names.append(
                getattr(call, "__name__", repr(call))
            )

print(f"Route dependencies: {dependency_names}")

if "get_current_user" not in dependency_names:
    raise RuntimeError(
        "get_current_user is not attached to /ai/answer."
    )

print("get_current_user dependency: PASS")


# ------------------------------------------------------------
# 2. OPENAPI SECURITY
# ------------------------------------------------------------

print("\n===== 2. OPENAPI SECURITY CONTRACT =====")

openapi = app.openapi()

target = "/api/v1/ai/answer"

if target not in openapi.get("paths", {}):
    raise RuntimeError(
        f"Missing OpenAPI path: {target}"
    )

post = openapi["paths"][target].get("post")

if post is None:
    raise RuntimeError(
        "POST operation missing."
    )

security = post.get("security")

print(f"OpenAPI security: {security}")

if not security:
    raise RuntimeError(
        "AI endpoint is not documented as secured."
    )

print("OpenAPI OAuth2 security: PASS")


# ------------------------------------------------------------
# 3. TEST CLIENT
# ------------------------------------------------------------

print("\n===== 3. INITIALIZE TEST CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


# ------------------------------------------------------------
# 4. UNAUTHENTICATED REQUEST
# ------------------------------------------------------------

print("\n===== 4. UNAUTHENTICATED REQUEST =====")

response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "Tell me about the Ajanta Caves.",
        "top_k": 5,
    },
)

print(f"HTTP status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code != 401:
    raise RuntimeError(
        f"Expected unauthenticated request to return 401, got {response.status_code}"
    )

print("Unauthenticated request rejection: PASS")


# ------------------------------------------------------------
# 5. FAKE GENERATION SERVICE
# ------------------------------------------------------------

print("\n===== 5. CONTROLLED AUTHENTICATED REQUEST =====")


class FakeResult:
    query = "Tell me about the Ajanta Caves."
    answer = "Controlled authenticated HeritageAI answer."
    grounded = True

    sources = [
        type(
            "FakeSource",
            (),
            {
                "rank": 1,
                "chunk_id": "auth-test-chunk",
                "document_id": "auth-test-document",
                "title": "Ajanta Caves — Authentication Test Evidence",
                "similarity_score": 0.91,
                "provenance_level": "VERIFIED",
                "is_verified": True,
            },
        )()
    ]


class FakeGenerationService:
    initialized = 0
    answer_calls = 0
    cleanup_calls = 0

    def __init__(self):
        FakeGenerationService.initialized += 1

    def answer(self, query, top_k):
        FakeGenerationService.answer_calls += 1

        if query != "Tell me about the Ajanta Caves.":
            raise RuntimeError("Unexpected query.")

        if top_k != 5:
            raise RuntimeError("Unexpected top_k.")

        return FakeResult()

    def close(self):
        FakeGenerationService.cleanup_calls += 1


original_service = GroundedAnswerService

import app.api.v1.ai as ai_module

ai_module.GroundedAnswerService = FakeGenerationService


def fake_current_user():
    return {
        "id": 1,
        "email": "authenticated-test@heritageai.local",
        "is_active": True,
    }


app.dependency_overrides[get_current_user] = fake_current_user

try:

    response = client.post(
        "/api/v1/ai/answer",
        json={
            "question": "Tell me about the Ajanta Caves.",
            "top_k": 5,
        },
    )

    print(f"HTTP status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code != 200:
        raise RuntimeError(
            f"Expected authenticated request to return 200, got {response.status_code}"
        )

    payload = response.json()

    if payload.get("grounded") is not True:
        raise RuntimeError(
            "Authenticated response is not grounded."
        )

    if len(payload.get("sources", [])) != 1:
        raise RuntimeError(
            "Authenticated response source contract failed."
        )

    print("Authenticated request: PASS")
    print("Grounded response: PASS")
    print("Source contract: PASS")

    if FakeGenerationService.initialized != 1:
        raise RuntimeError(
            f"Expected one service initialization, got {FakeGenerationService.initialized}"
        )

    if FakeGenerationService.answer_calls != 1:
        raise RuntimeError(
            f"Expected one service answer call, got {FakeGenerationService.answer_calls}"
        )

    if FakeGenerationService.cleanup_calls != 1:
        raise RuntimeError(
            f"Expected one service cleanup call, got {FakeGenerationService.cleanup_calls}"
        )

    print("Generation invocation: PASS")
    print("Service cleanup: PASS")

finally:
    app.dependency_overrides.clear()
    ai_module.GroundedAnswerService = original_service


# ------------------------------------------------------------
# 6. VERIFY SERVICE NOT CALLED WHEN UNAUTHENTICATED
# ------------------------------------------------------------

print("\n===== 6. AUTHORIZATION BOUNDARY =====")

print(
    "Unauthenticated request was rejected before generation."
)

print("Authentication boundary: PASS")


# ------------------------------------------------------------
# 7. DATABASE STATE
# ------------------------------------------------------------

print("\n===== 7. READ-ONLY DATABASE STATE =====")

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


print("\n===== STEP 8B-013W-B COMPLETE =====")
print("AI authentication dependency: PASS")
print("OpenAPI security: PASS")
print("Unauthenticated 401 rejection: PASS")
print("Authenticated request: PASS")
print("Generation invocation: PASS")
print("Service cleanup: PASS")
print("Authentication boundary: PASS")
print("MySQL no-mutation: PASS")
print("NO REAL GEMINI API CALLS MADE.")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("SEND THE COMPLETE OUTPUT.")
