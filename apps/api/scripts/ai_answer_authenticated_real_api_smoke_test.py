from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.contracts.ai import (
    GroundedAnswerRequest,
    GroundedAnswerResponse,
)
from app.dependencies import get_current_user
from app.core.config import settings


print("===== STEP 8B-013W-C — REAL AUTHENTICATED AI API SMOKE TEST =====")


# ============================================================
# 1. VERIFY PRODUCTION MODEL
# ============================================================

print("\n===== 1. VERIFY PRODUCTION MODEL =====")

print(f"Configured generation model: {settings.GEMINI_GENERATION_MODEL}")

if settings.GEMINI_GENERATION_MODEL != "gemini-3.5-flash":
    raise RuntimeError(
        "Unexpected production generation model."
    )

print("Production model: PASS")


# ============================================================
# 2. DATABASE PRE-TEST STATE
# ============================================================

print("\n===== 2. PRE-TEST DATABASE STATE =====")

from sqlalchemy import text
from app.db.session import SessionLocal

db = SessionLocal()

try:
    documents_before = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_documents")
    ).scalar_one()

    chunks_before = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_chunks")
    ).scalar_one()

    embeddings_before = db.execute(
        text("SELECT COUNT(*) FROM ai_embeddings")
    ).scalar_one()

finally:
    db.close()

print(f"Knowledge documents: {documents_before}")
print(f"Knowledge chunks: {chunks_before}")
print(f"AI embeddings: {embeddings_before}")

if (documents_before, chunks_before, embeddings_before) != (89, 89, 89):
    raise RuntimeError(
        "Unexpected pre-test database state."
    )

print("DATABASE PRECONDITION: PASS")


# ============================================================
# 3. FASTAPI CLIENT
# ============================================================

print("\n===== 3. INITIALIZE FASTAPI CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


# ============================================================
# 4. VERIFY UNAUTHENTICATED BOUNDARY
# ============================================================

print("\n===== 4. VERIFY UNAUTHENTICATED BOUNDARY =====")

unauthenticated_response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "Tell me about the Ajanta Caves.",
        "top_k": 5,
    },
)

print(
    f"Unauthenticated HTTP status: "
    f"{unauthenticated_response.status_code}"
)

if unauthenticated_response.status_code != 401:
    raise RuntimeError(
        "Unauthenticated AI request did not return HTTP 401."
    )

print("Unauthenticated access rejection: PASS")


# ============================================================
# 5. CREATE REAL TEST USER / TOKEN
# ============================================================

print("\n===== 5. AUTHENTICATE REAL TEST USER =====")

# Discover the existing login implementation rather than
# bypassing authentication with dependency overrides.

TEST_EMAIL = "heritageai.ai.smoke.test@gmail.com"
TEST_PASSWORD = "HeritageAI_Smoke_2026!"

register_response = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": "HeritageAI Authentication Smoke Test",
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
    },
)

print(
    f"Registration HTTP status: "
    f"{register_response.status_code}"
)

if register_response.status_code not in (200, 201, 400, 409):
    raise RuntimeError(
        "Unexpected registration response."
    )

# Login must succeed whether the test user was newly created
# or already existed.

login_response = client.post(
    "/api/v1/auth/login",
    data={
        "username": TEST_EMAIL,
        "password": TEST_PASSWORD,
    },
)

print(
    f"Login HTTP status: "
    f"{login_response.status_code}"
)

if login_response.status_code != 200:
    raise RuntimeError(
        "Real authentication failed."
    )

login_payload = login_response.json()

if "access_token" not in login_payload:
    raise RuntimeError(
        "Login response does not contain access_token."
    )

access_token = login_payload["access_token"]

if not access_token:
    raise RuntimeError(
        "Received empty access token."
    )

print("Real authentication: PASS")
print("JWT access token received: PASS")


# ============================================================
# 6. AUTHENTICATED REAL AI REQUEST
# ============================================================

print("\n===== 6. REAL AUTHENTICATED GEMINI REQUEST =====")

question = "Tell me about the Ajanta Caves."

print(f"Question: {question}")
print("top_k: 5")
print("REAL GEMINI REQUEST: START")

authenticated_response = client.post(
    "/api/v1/ai/answer",
    headers={
        "Authorization": f"Bearer {access_token}",
    },
    json={
        "question": question,
        "top_k": 5,
    },
)

print("REAL GEMINI REQUEST: COMPLETED")

print(
    f"HTTP status: "
    f"{authenticated_response.status_code}"
)

if authenticated_response.status_code != 200:
    print(
        f"Response: {authenticated_response.text}"
    )

    raise RuntimeError(
        "Authenticated real AI request failed."
    )

payload = authenticated_response.json()


# ============================================================
# 7. RESPONSE CONTRACT
# ============================================================

print("\n===== 7. RESPONSE CONTRACT =====")

required_fields = {
    "query",
    "answer",
    "sources",
    "grounded",
}

missing_fields = required_fields - set(payload.keys())

if missing_fields:
    raise RuntimeError(
        f"Missing response fields: {sorted(missing_fields)}"
    )

if payload["query"] != question:
    raise RuntimeError(
        "Response query does not match request."
    )

if not isinstance(payload["answer"], str):
    raise RuntimeError(
        "Answer is not a string."
    )

if not payload["answer"].strip():
    raise RuntimeError(
        "Answer is empty."
    )

if payload["grounded"] is not True:
    raise RuntimeError(
        "Ajanta request was not grounded."
    )

if not isinstance(payload["sources"], list):
    raise RuntimeError(
        "Sources is not a list."
    )

if len(payload["sources"]) != 5:
    raise RuntimeError(
        f"Expected five sources, got {len(payload['sources'])}"
    )

print(f"Grounded: {payload['grounded']}")
print(f"Answer length: {len(payload['answer'])}")
print(f"Sources returned: {len(payload['sources'])}")

print("Response contract: PASS")


# ============================================================
# 8. SOURCE CONTRACT
# ============================================================

print("\n===== 8. SOURCE VALIDATION =====")

required_source_fields = {
    "rank",
    "chunk_id",
    "document_id",
    "title",
    "similarity_score",
    "provenance_level",
    "is_verified",
}

ajanta_evidence = False

for source in payload["sources"]:

    missing = required_source_fields - set(source.keys())

    if missing:
        raise RuntimeError(
            f"Source missing fields: {sorted(missing)}"
        )

    if "Ajanta" in str(source["title"]):
        ajanta_evidence = True

    print(
        f"Rank {source['rank']} | "
        f"Score {source['similarity_score']} | "
        f"{source['title']} | "
        f"Verified={source['is_verified']}"
    )

if not ajanta_evidence:
    raise RuntimeError(
        "No Ajanta evidence returned."
    )

print("Source contract: PASS")
print("Ajanta evidence presence: PASS")


# ============================================================
# 9. API METADATA BOUNDARY
# ============================================================

print("\n===== 9. API METADATA BOUNDARY =====")

serialized = str(payload).lower()

for forbidden in (
    "qdrant",
    "embedding",
    "vector",
    "retrieval",
):
    if forbidden in serialized:
        raise RuntimeError(
            f"Internal API metadata leaked: {forbidden}"
        )

# These two are legitimate public source fields.
# Therefore they are intentionally allowed:
#
# similarity_score
# provenance_level

print("Internal retrieval metadata hidden: PASS")


# ============================================================
# 10. GENERATED ANSWER
# ============================================================

print("\n===== 10. GENERATED ANSWER =====")
print(payload["answer"])


# ============================================================
# 11. DATABASE POST-TEST STATE
# ============================================================

print("\n===== 11. POST-TEST DATABASE STATE =====")

db = SessionLocal()

try:
    documents_after = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_documents")
    ).scalar_one()

    chunks_after = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_chunks")
    ).scalar_one()

    embeddings_after = db.execute(
        text("SELECT COUNT(*) FROM ai_embeddings")
    ).scalar_one()

finally:
    db.close()

print(f"Knowledge documents: {documents_after}")
print(f"Knowledge chunks: {chunks_after}")
print(f"AI embeddings: {embeddings_after}")

if (
    documents_after,
    chunks_after,
    embeddings_after,
) != (
    documents_before,
    chunks_before,
    embeddings_before,
):
    raise RuntimeError(
        "Database state changed during API request."
    )

print("MYSQL NO-MUTATION CHECK: PASS")


# ============================================================
# 12. FINAL RESULT
# ============================================================

print("\n===== STEP 8B-013W-C COMPLETE =====")
print("Production model: gemini-3.5-flash")
print("Real authentication: PASS")
print("JWT authentication: PASS")
print("Unauthenticated 401 boundary: PASS")
print("Authenticated AI endpoint: PASS")
print("Real Gemini generation: PASS")
print("Grounded response: PASS")
print("Five-source response: PASS")
print("Ajanta evidence retrieval: PASS")
print("API metadata boundary: PASS")
print("MySQL no-mutation: PASS")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("DO NOT RUN THE FULL 6-CASE REGRESSION YET.")
print("SEND THE COMPLETE OUTPUT.")
