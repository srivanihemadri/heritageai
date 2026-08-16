from pathlib import Path
import inspect

from app.core.config import settings
from app.main import app
from app.api.v1.ai import router as ai_router
from app.api.v1.contracts.ai import (
    GroundedAnswerRequest,
    GroundedAnswerResponse,
    GroundedAnswerSourceResponse,
    GroundedAnswerErrorResponse,
)
from app.services.ai.generation import GroundedAnswerService
from app.services.ai.retrieval import RAGRetrievalService
from app.services.ai.retrieval.relevance_gate import (
    RetrievalRelevanceGate,
    RelevanceDecision,
)
from sqlalchemy import text
from app.db.session import SessionLocal


print("===== STEP 8B-013V-U — PRODUCTION AI API FINAL ARCHITECTURE AUDIT =====")


print("\n===== 1. PRODUCTION MODEL =====")

print(f"Generation model: {settings.GEMINI_GENERATION_MODEL}")

if settings.GEMINI_GENERATION_MODEL != "gemini-3.5-flash":
    raise RuntimeError(
        f"Unexpected production model: {settings.GEMINI_GENERATION_MODEL}"
    )

print("Production model: PASS")


print("\n===== 2. AI ROUTER CONTRACT =====")

router_matches = [
    route
    for route in ai_router.routes
    if getattr(route, "path", None) == "/ai/answer"
    and "POST" in getattr(route, "methods", set())
]

print(f"AI router routes: {len(ai_router.routes)}")
print(f"POST /ai/answer: {len(router_matches)}")
print(f"Router prefix: {ai_router.prefix}")

if len(router_matches) != 1:
    raise RuntimeError(
        f"Expected exactly one POST /ai/answer, found {len(router_matches)}"
    )

if ai_router.prefix != "/ai":
    raise RuntimeError(
        f"Unexpected AI router prefix: {ai_router.prefix}"
    )

print("AI router contract: PASS")


print("\n===== 3. OPENAPI CONTRACT =====")

openapi = app.openapi()
paths = openapi.get("paths", {})

target = "/api/v1/ai/answer"

if target not in paths:
    raise RuntimeError(f"Missing OpenAPI path: {target}")

post = paths[target].get("post")

if post is None:
    raise RuntimeError(f"Missing POST operation: {target}")

print(f"OpenAPI {target}: PASS")
print("POST operation: PASS")

for code in ("200", "422", "500"):
    if code not in post.get("responses", {}):
        raise RuntimeError(
            f"Missing HTTP {code} response declaration."
        )

    print(f"HTTP {code} declaration: PASS")

if "requestBody" not in post:
    raise RuntimeError("Request body declaration missing.")

print("Request body schema: PASS")
print("OpenAPI contract: PASS")


print("\n===== 4. API CONTRACT MODELS =====")

print("GroundedAnswerRequest: PASS")
print("GroundedAnswerResponse: PASS")
print("GroundedAnswerSourceResponse: PASS")
print("GroundedAnswerErrorResponse: PASS")

request = GroundedAnswerRequest(
    question="Tell me about the Ajanta Caves.",
    top_k=5,
)

if request.question != "Tell me about the Ajanta Caves.":
    raise RuntimeError("Request question contract failed.")

if request.top_k != 5:
    raise RuntimeError("Request top_k contract failed.")

print("Request contract behavior: PASS")


print("\n===== 5. GENERATION SERVICE ARCHITECTURE =====")

print("GroundedAnswerService import: PASS")
print("RAGRetrievalService import: PASS")
print("RetrievalRelevanceGate import: PASS")
print("RelevanceDecision import: PASS")

service = GroundedAnswerService()

try:
    attributes = vars(service)

    retrieval_attributes = [
        name
        for name, value in attributes.items()
        if isinstance(value, RAGRetrievalService)
    ]

    gate_attributes = [
        name
        for name, value in attributes.items()
        if isinstance(value, RetrievalRelevanceGate)
    ]

    print(
        "RAGRetrievalService attributes:",
        retrieval_attributes,
    )

    print(
        "RetrievalRelevanceGate attributes:",
        gate_attributes,
    )

    if retrieval_attributes != ["retrieval"]:
        raise RuntimeError(
            f"Unexpected retrieval architecture: {retrieval_attributes}"
        )

    if gate_attributes != ["relevance_gate"]:
        raise RuntimeError(
            f"Unexpected relevance gate architecture: {gate_attributes}"
        )

    if service.model != "gemini-3.5-flash":
        raise RuntimeError(
            f"Unexpected service model: {service.model}"
        )

    print("RAG retrieval integration: PASS")
    print("Relevance gate integration: PASS")
    print("Generation service model: PASS")

finally:
    service.close()

print("Generation service architecture: PASS")


print("\n===== 6. GATE ORDERING =====")

source = inspect.getsource(GroundedAnswerService.answer)

gate_position = source.find("relevance_gate.evaluate")

generation_positions = [
    position
    for position in (
        source.find("generate_content"),
        source.find("generate_content_stream"),
    )
    if position != -1
]

if gate_position == -1:
    raise RuntimeError(
        "Relevance gate evaluation not found."
    )

if not generation_positions:
    raise RuntimeError(
        "Gemini generation call not found."
    )

generation_position = min(generation_positions)

print(f"Relevance gate position: {gate_position}")
print(f"Gemini generation position: {generation_position}")

if gate_position >= generation_position:
    raise RuntimeError(
        "Relevance gate does not precede Gemini generation."
    )

print("Relevance gate precedes Gemini generation: PASS")


print("\n===== 7. PRODUCTION / TEST SEPARATION =====")

production_root = Path(
    r"D:\PROJECT\heritageai\apps\api\app"
)

forbidden = [
    "ai_answer_real_api",
    "ai_answer_end_to_end_regression",
    "ai_grounding_quality_test",
    "FakeGenerationService",
    "ControlledAnswerService",
]

violations = []

for path in production_root.rglob("*.py"):
    content = path.read_text(encoding="utf-8")

    for value in forbidden:
        if value in content:
            violations.append(
                f"{path}: {value}"
            )

if violations:
    for violation in violations:
        print(violation)

    raise RuntimeError(
        "Production/test separation violation detected."
    )

print("Production/test separation: PASS")


print("\n===== 8. AI ENDPOINT UNIQUENESS =====")

ai_matches = [
    path
    for path in openapi.get("paths", {})
    if path == "/api/v1/ai/answer"
]

print(f"OpenAPI AI endpoint matches: {len(ai_matches)}")

if len(ai_matches) != 1:
    raise RuntimeError(
        f"Expected exactly one AI endpoint, found {len(ai_matches)}"
    )

print("AI endpoint uniqueness: PASS")


print("\n===== 9. EXISTING API ROUTER ARCHITECTURE =====")

router_directory = Path(
    r"D:\PROJECT\heritageai\apps\api\app\api\v1"
)

required_routers = [
    "auth.py",
    "health.py",
    "heritage_sites.py",
    "users.py",
    "ai.py",
]

for filename in required_routers:
    path = router_directory / filename

    if not path.exists():
        raise RuntimeError(
            f"Missing router: {filename}"
        )

    print(f"{filename}: PASS")

print("Existing API router architecture: PASS")


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


print("\n===== 11. FINAL SAFETY CHECK =====")

print("NO GEMINI GENERATION CALL MADE.")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO PRODUCTION SOURCE CHANGES MADE.")
print("NO CONFIGURATION CHANGES MADE.")

print("\n===== STEP 8B-013V-U-RECOVERY COMPLETE =====")
print("Canonical architecture audit script: CREATED")
print("Production architecture references: CORRECT")
print("service.retrieval: PASS")
print("service.relevance_gate: PASS")
print("NO GEMINI GENERATION CALLS MADE.")
print("NO DATABASE CHANGES MADE.")
print("NO QDRANT CHANGES MADE.")
print("DO NOT RUN THE FULL REAL API REGRESSION.")
print("SEND THE COMPLETE OUTPUT.")
