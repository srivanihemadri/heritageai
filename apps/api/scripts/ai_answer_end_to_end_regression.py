from fastapi.testclient import TestClient

from app.main import app


EXPECTED_DOCUMENTS = 89
EXPECTED_CHUNKS = 89
EXPECTED_EMBEDDINGS = 89


def get_db_state():
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

        return documents, chunks, embeddings

    finally:
        db.close()


def assert_db_state(label):
    documents, chunks, embeddings = get_db_state()

    print(f"{label} DATABASE STATE")
    print(f"Knowledge documents: {documents}")
    print(f"Knowledge chunks: {chunks}")
    print(f"AI embeddings: {embeddings}")

    if documents != EXPECTED_DOCUMENTS:
        raise RuntimeError(
            f"Knowledge document count changed: {documents}"
        )

    if chunks != EXPECTED_CHUNKS:
        raise RuntimeError(
            f"Knowledge chunk count changed: {chunks}"
        )

    if embeddings != EXPECTED_EMBEDDINGS:
        raise RuntimeError(
            f"Embedding count changed: {embeddings}"
        )

    print("MYSQL STATE: PASS")


def assert_source_contract(response_json):
    sources = response_json.get("sources")

    if not isinstance(sources, list):
        raise RuntimeError("sources is not a list.")

    if len(sources) != 5:
        raise RuntimeError(
            f"Expected 5 sources, got {len(sources)}"
        )

    ranks = [source["rank"] for source in sources]

    if ranks != [1, 2, 3, 4, 5]:
        raise RuntimeError(
            f"Invalid source ranks: {ranks}"
        )

    for source in sources:
        required = [
            "rank",
            "chunk_id",
            "document_id",
            "title",
            "similarity_score",
            "provenance_level",
            "is_verified",
        ]

        for field in required:
            if field not in source:
                raise RuntimeError(
                    f"Missing source field: {field}"
                )

        if not isinstance(
            source["similarity_score"],
            (int, float),
        ):
            raise RuntimeError(
                "similarity_score is not numeric."
            )


def assert_no_internal_metadata(response_json):
    if not isinstance(response_json, dict):
        raise RuntimeError(
            "API response is not a JSON object."
        )

    allowed_top_level_fields = {
        "query",
        "answer",
        "sources",
        "grounded",
    }

    unexpected_fields = (
        set(response_json.keys())
        - allowed_top_level_fields
    )

    if unexpected_fields:
        raise RuntimeError(
            "Unexpected top-level response fields: "
            f"{sorted(unexpected_fields)}"
        )

    sources = response_json.get("sources", [])

    if not isinstance(sources, list):
        raise RuntimeError(
            "sources must be a list."
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

    for source in sources:
        if not isinstance(source, dict):
            raise RuntimeError(
                "Source entry is not a JSON object."
            )

        unexpected_source_fields = (
            set(source.keys())
            - allowed_source_fields
        )

        if unexpected_source_fields:
            raise RuntimeError(
                "Unexpected source fields: "
                f"{sorted(unexpected_source_fields)}"
            )

    print("Internal retrieval metadata hidden: PASS")


client = TestClient(app)

assert_db_state("PRE-TEST")


tests = [
    {
        "name": "SUPPORTED_DIRECT",
        "question": "Tell me about the Ajanta Caves.",
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "SUPPORTED_CROSS_SITE",
        "question": (
            "What is the relationship between "
            "Ajanta Caves and Ellora Caves?"
        ),
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "SUPPORTED_HISTORICAL",
        "question": (
            "Tell me about the historical events "
            "associated with the Red Fort."
        ),
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "UNSUPPORTED_SPECIFIC",
        "question": (
            "What was the exact construction cost "
            "of the Ajanta Caves in ancient Indian currency?"
        ),
        "expected_grounded": False,
        "expected_sources": 0,
    },
    {
        "name": "UNRELATED",
        "question": "What is the capital of Japan?",
        "expected_grounded": False,
        "expected_sources": 0,
    },
    {
        "name": "MISLEADING",
        "question": "Was Ajanta Caves built by the Mughal Empire?",
        "expected_grounded": True,
        "expected_sources": 5,
    },
]


print("\n===== STEP 8B-013V-I — END-TO-END API REGRESSION =====")

for index, test in enumerate(tests, start=1):

    print(
        f"\n===== TEST {index}/{len(tests)} — "
        f"{test['name']} ====="
    )

    print(f"Question: {test['question']}")

    response = client.post(
        "/api/v1/ai/answer",
        json={
            "question": test["question"],
            "top_k": 5,
        },
    )

    print(f"HTTP status: {response.status_code}")

    if response.status_code != 200:
        raise RuntimeError(
            f"{test['name']}: expected HTTP 200, "
            f"got {response.status_code}"
        )

    payload = response.json()

    grounded = payload.get("grounded")
    sources = payload.get("sources", [])
    answer = payload.get("answer", "")

    print(f"Grounded: {grounded}")
    print(f"Answer length: {len(answer)}")
    print(f"Sources returned: {len(sources)}")

    if grounded != test["expected_grounded"]:
        raise RuntimeError(
            f"{test['name']}: expected grounded="
            f"{test['expected_grounded']}, "
            f"got {grounded}"
        )

    if len(sources) != test["expected_sources"]:
        raise RuntimeError(
            f"{test['name']}: expected "
            f"{test['expected_sources']} sources, "
            f"got {len(sources)}"
        )

    if not answer.strip():
        raise RuntimeError(
            f"{test['name']}: empty answer."
        )

    if test["expected_sources"] == 5:
        assert_source_contract(payload)

        print("Source contract: PASS")

    else:
        if sources:
            raise RuntimeError(
                f"{test['name']}: rejected answer "
                "must contain zero sources."
            )

        print("Zero-source rejection contract: PASS")

    assert_no_internal_metadata(payload)

    print(f"{test['name']}: PASS")


print("\n===== INVALID REQUEST REGRESSION =====")

response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "",
        "top_k": 5,
    },
)

print(f"Empty question HTTP status: {response.status_code}")

if response.status_code != 422:
    raise RuntimeError(
        "Empty question should return HTTP 422."
    )

print("Empty question: PASS")


response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "Tell me about Ajanta.",
        "top_k": 0,
    },
)

print(f"Invalid top_k HTTP status: {response.status_code}")

if response.status_code != 422:
    raise RuntimeError(
        "Invalid top_k should return HTTP 422."
    )

print("Invalid top_k: PASS")


response = client.post(
    "/api/v1/ai/answer",
    json={
        "question": "Tell me about Ajanta.",
        "top_k": 5,
        "unexpected_field": True,
    },
)

print(
    f"Unknown field HTTP status: "
    f"{response.status_code}"
)

if response.status_code != 422:
    raise RuntimeError(
        "Unknown field should return HTTP 422."
    )

print("Unknown field: PASS")


assert_db_state("\nPOST-TEST")

print("\n===== STEP 8B-013V-I COMPLETE =====")
print("End-to-end API regression: PASS")
print("Supported direct query: PASS")
print("Supported cross-site query: PASS")
print("Supported historical query: PASS")
print("Unsupported query rejection: PASS")
print("Unrelated query rejection: PASS")
print("Misleading claim handling: PASS")
print("Source contract: PASS")
print("Grounding safety: PASS")
print("Request validation: PASS")
print("MySQL no-mutation: PASS")
print("NO EMBEDDINGS CREATED.")
print("NO QDRANT CHANGES MADE.")
print("SEND THE COMPLETE OUTPUT.")
