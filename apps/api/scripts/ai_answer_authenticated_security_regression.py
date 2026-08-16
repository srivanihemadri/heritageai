from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

from sqlalchemy import text
from app.db.session import SessionLocal


print("===== STEP 8B-013W-D — AUTHENTICATED AI SECURITY REGRESSION =====")


TEST_EMAIL = "heritageai.ai.smoke.test@gmail.com"
TEST_PASSWORD = "HeritageAI_Smoke_2026!"

QUESTION = "Tell me about the Ajanta Caves."


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
# 2. PRE-TEST DATABASE STATE
# ============================================================

print("\n===== 2. PRE-TEST DATABASE STATE =====")

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

if (
    documents_before,
    chunks_before,
    embeddings_before,
) != (89, 89, 89):
    raise RuntimeError(
        "Unexpected database precondition."
    )

print("MYSQL PRECONDITION: PASS")


# ============================================================
# 3. FASTAPI CLIENT
# ============================================================

print("\n===== 3. INITIALIZE FASTAPI CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


# ============================================================
# 4. NO AUTHORIZATION HEADER
# ============================================================

print("\n===== TEST 1/4 — NO AUTHORIZATION HEADER =====")

response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": QUESTION,
        "top_k": 5,
    },
)

print(f"HTTP status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401 without token, got {response.status_code}"
    )

print("No-token rejection: PASS")


# ============================================================
# 5. MALFORMED BEARER TOKEN
# ============================================================

print("\n===== TEST 2/4 — MALFORMED BEARER TOKEN =====")

response = client.post(
    "/api/v1/ai/answer",
    headers={
        "Authorization": "Bearer",
    },
    json={
        "question": QUESTION,
        "top_k": 5,
    },
)

print(f"HTTP status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401 for malformed token, got {response.status_code}"
    )

print("Malformed-token rejection: PASS")


# ============================================================
# 6. INVALID JWT
# ============================================================

print("\n===== TEST 3/4 — INVALID JWT =====")

response = client.post(
    "/api/v1/ai/answer",
    headers={
        "Authorization": "Bearer invalid.jwt.token",
    },
    json={
        "question": QUESTION,
        "top_k": 5,
    },
)

print(f"HTTP status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401 for invalid JWT, got {response.status_code}"
    )

print("Invalid-token rejection: PASS")


# ============================================================
# 7. REAL LOGIN
# ============================================================

print("\n===== 7. REAL AUTHENTICATION =====")

login_response = client.post(
    "/api/v1/auth/login",
    data={
        "username": TEST_EMAIL,
        "password": TEST_PASSWORD,
    },
)

print(f"Login HTTP status: {login_response.status_code}")

if login_response.status_code != 200:
    print(login_response.text)
    raise RuntimeError(
        "Real login failed."
    )

login_payload = login_response.json()

if "access_token" not in login_payload:
    raise RuntimeError(
        "Login response missing access_token."
    )

access_token = login_payload["access_token"]

if not access_token:
    raise RuntimeError(
        "Empty access token."
    )

print("Real login: PASS")
print("JWT acquisition: PASS")


# ============================================================
# 8. VALID JWT — REAL GEMINI REQUEST
# ============================================================

print("\n===== TEST 4/4 — VALID JWT + REAL GEMINI =====")

print(f"Question: {QUESTION}")
print("top_k: 5")
print("REAL GEMINI REQUEST: START")

response = client.post(
    "/api/v1/ai/answer",
    headers={
        "Authorization": f"Bearer {access_token}",
    },
    json={
        "question": QUESTION,
        "top_k": 5,
    },
)

print("REAL GEMINI REQUEST: COMPLETED")

print(f"HTTP status: {response.status_code}")

if response.status_code != 200:
    print(f"Response: {response.text}")
    raise RuntimeError(
        f"Expected HTTP 200 for valid JWT, got {response.status_code}"
    )

payload = response.json()


# ============================================================
# 9. RESPONSE CONTRACT
# ============================================================

print("\n===== 9. AUTHENTICATED RESPONSE CONTRACT =====")

required_fields = {
    "query",
    "answer",
    "sources",
    "grounded",
}

missing = required_fields - set(payload.keys())

if missing:
    raise RuntimeError(
        f"Missing response fields: {sorted(missing)}"
    )

if payload["query"] != QUESTION:
    raise RuntimeError(
        "Query mismatch."
    )

if payload["grounded"] is not True:
    raise RuntimeError(
        "Authenticated response is not grounded."
    )

if not isinstance(payload["answer"], str):
    raise RuntimeError(
        "Answer is not a string."
    )

if not payload["answer"].strip():
    raise RuntimeError(
        "Answer is empty."
    )

if len(payload["sources"]) != 5:
    raise RuntimeError(
        f"Expected 5 sources, got {len(payload['sources'])}"
    )

print(f"Grounded: {payload['grounded']}")
print(f"Answer length: {len(payload['answer'])}")
print(f"Sources returned: {len(payload['sources'])}")

print("Authenticated response contract: PASS")


# ============================================================
# 10. SOURCE VALIDATION
# ============================================================

print("\n===== 10. SOURCE VALIDATION =====")

required_source_fields = {
    "rank",
    "chunk_id",
    "document_id",
    "title",
    "similarity_score",
    "provenance_level",
    "is_verified",
}

ajanta_found = False

for source in payload["sources"]:

    missing = required_source_fields - set(source.keys())

    if missing:
        raise RuntimeError(
            f"Source missing fields: {sorted(missing)}"
        )

    if "Ajanta" in str(source["title"]):
        ajanta_found = True

    print(
        f"Rank {source['rank']} | "
        f"Score {source['similarity_score']} | "
        f"{source['title']} | "
        f"Verified={source['is_verified']}"
    )

if not ajanta_found:
    raise RuntimeError(
        "Ajanta evidence not present."
    )

print("Source contract: PASS")
print("Ajanta evidence presence: PASS")


# ============================================================
# 11. API METADATA BOUNDARY
# ============================================================

print("\n===== 11. API METADATA BOUNDARY =====")

serialized = str(payload).lower()

for forbidden in (
    "qdrant",
    "embedding",
    "vector",
    "retrieval",
):
    if forbidden in serialized:
        raise RuntimeError(
            f"Internal metadata leaked: {forbidden}"
        )

print("Internal retrieval metadata hidden: PASS")


# ============================================================
# 12. ANSWER
# ============================================================

print("\n===== 12. GENERATED ANSWER =====")
print(payload["answer"])


# ============================================================
# 13. POST-TEST DATABASE STATE
# ============================================================

print("\n===== 13. POST-TEST DATABASE STATE =====")

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
        "Database state changed during security regression."
    )

print("MYSQL NO-MUTATION CHECK: PASS")


# ============================================================
# 14. FINAL RESULT
# ============================================================

print("\n===== STEP 8B-013W-D COMPLETE =====")
print("No-token rejection: PASS")
print("Malformed-token rejection: PASS")
print("Invalid-JWT rejection: PASS")
print("Real login: PASS")
print("JWT authentication: PASS")
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
