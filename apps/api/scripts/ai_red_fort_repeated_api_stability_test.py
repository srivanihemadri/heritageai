from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from sqlalchemy import text


QUESTION = "Tell me about the historical events associated with the Red Fort."
TOP_K = 5


def database_state():
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

        return documents, chunks, embeddings

    finally:
        db.close()


def validate_metadata_boundary(payload):
    allowed_top_level = {
        "query",
        "answer",
        "sources",
        "grounded",
    }

    unexpected_top_level = (
        set(payload.keys()) - allowed_top_level
    )

    if unexpected_top_level:
        raise RuntimeError(
            f"Unexpected top-level fields: {unexpected_top_level}"
        )

    allowed_source_fields = {
        "rank",
        "chunk_id",
        "document_id",
        "title",
        "similarity_score",
        "provenance_level",
        "is_verified",
    }

    forbidden_strings = {
        "qdrant",
        "embedding",
        "vector",
        "internal",
    }

    serialized_answer = str(payload.get("answer", "")).lower()

    for value in forbidden_strings:
        if value in serialized_answer:
            raise RuntimeError(
                f"Forbidden metadata leaked into answer: {value}"
            )

    for source in payload.get("sources", []):
        unexpected_source = (
            set(source.keys()) - allowed_source_fields
        )

        if unexpected_source:
            raise RuntimeError(
                f"Unexpected source fields: {unexpected_source}"
            )


print("===== STEP 8B-013V-Q — RED FORT API STABILITY TEST =====")

print("\n===== 1. PRE-TEST DATABASE STATE =====")

before = database_state()

print(f"Knowledge documents: {before[0]}")
print(f"Knowledge chunks: {before[1]}")
print(f"AI embeddings: {before[2]}")

if before != (89, 89, 89):
    raise RuntimeError(
        f"Unexpected pre-test database state: {before}"
    )

print("DATABASE PRECONDITION: PASS")


print("\n===== 2. INITIALIZE FASTAPI CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


print("\n===== 3. THREE SEQUENTIAL RED FORT REQUESTS =====")

results = []

for attempt in range(1, 4):

    print(
        f"\n===== RED FORT ATTEMPT {attempt}/3 ====="
    )

    print(f"Question: {QUESTION}")
    print(f"top_k: {TOP_K}")
    print("REAL GEMINI REQUEST: START")

    response = client.post(
        "/api/v1/ai/answer",
        json={
            "question": QUESTION,
            "top_k": TOP_K,
        },
    )

    print("REAL GEMINI REQUEST: COMPLETED")
    print(f"HTTP status: {response.status_code}")

    if response.status_code != 200:
        print(f"Response: {response.text}")

        raise RuntimeError(
            f"Attempt {attempt}: expected HTTP 200, "
            f"got {response.status_code}"
        )

    payload = response.json()

    if payload.get("grounded") is not True:
        raise RuntimeError(
            f"Attempt {attempt}: expected grounded=True"
        )

    sources = payload.get("sources", [])

    if len(sources) != 5:
        raise RuntimeError(
            f"Attempt {attempt}: expected 5 sources, "
            f"got {len(sources)}"
        )

    if payload.get("query") != QUESTION:
        raise RuntimeError(
            f"Attempt {attempt}: query mismatch"
        )

    if not payload.get("answer"):
        raise RuntimeError(
            f"Attempt {attempt}: empty answer"
        )

    validate_metadata_boundary(payload)

    print(f"Grounded: {payload['grounded']}")
    print(f"Answer length: {len(payload['answer'])}")
    print(f"Sources returned: {len(sources)}")
    print("Response contract: PASS")
    print("Safety boundary: PASS")

    results.append(payload)


print("\n===== 4. STABILITY SUMMARY =====")

print(f"Requests executed: {len(results)}")
print("Successful requests: 3/3")

if len(results) != 3:
    raise RuntimeError(
        "Expected exactly 3 successful requests."
    )

print("RED FORT API STABILITY: PASS")


print("\n===== 5. POST-TEST DATABASE STATE =====")

after = database_state()

print(f"Knowledge documents: {after[0]}")
print(f"Knowledge chunks: {after[1]}")
print(f"AI embeddings: {after[2]}")

if after != before:
    raise RuntimeError(
        f"Database mutation detected: before={before}, after={after}"
    )

print("MYSQL NO-MUTATION CHECK: PASS")


print("\n===== STEP 8B-013V-Q COMPLETE =====")
print("Three Red Fort API requests: PASS")
print("HTTP 200 stability: PASS")
print("Grounded response validation: PASS")
print("Five-source validation: PASS")
print("API metadata boundary: PASS")
print("MySQL no-mutation: PASS")
print("NO CONFIGURATION CHANGES MADE.")
print("NO SOURCE CHANGES MADE.")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("DO NOT RUN THE FULL 6-CASE REGRESSION YET.")
print("SEND THE COMPLETE OUTPUT.")
