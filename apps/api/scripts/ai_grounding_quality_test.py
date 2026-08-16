from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.ai.generation import GroundedAnswerService


TEST_CASES = [
    {
        "name": "SUPPORTED_DIRECT",
        "query": "Tell me about the Ajanta Caves.",
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "SUPPORTED_CROSS_SITE",
        "query": "What is the relationship between Ajanta Caves and Ellora Caves?",
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "SUPPORTED_HISTORICAL",
        "query": "Tell me about the historical events associated with the Red Fort.",
        "expected_grounded": True,
        "expected_sources": 5,
    },
    {
        "name": "UNSUPPORTED_SPECIFIC",
        "query": "What was the exact construction cost of the Ajanta Caves in ancient Indian currency?",
        "expected_grounded": False,
        "expected_sources": 0,
    },
    {
        "name": "UNRELATED",
        "query": "What is the capital of Japan?",
        "expected_grounded": False,
        "expected_sources": 0,
    },
    {
        "name": "MISLEADING",
        "query": "Was Ajanta Caves built by the Mughal Empire?",
        "expected_grounded": True,
        "expected_sources": 5,
    },
]


db = SessionLocal()
service = None

try:

    print("===== 1. PRE-TEST DATABASE STATE =====")

    documents_before = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_documents")
    ).scalar_one()

    chunks_before = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_chunks")
    ).scalar_one()

    embeddings_before = db.execute(
        text("SELECT COUNT(*) FROM ai_embeddings")
    ).scalar_one()

    print("Knowledge documents:", documents_before)
    print("Knowledge chunks:", chunks_before)
    print("AI embeddings:", embeddings_before)

    if documents_before != 89:
        raise RuntimeError(
            f"Expected 89 knowledge documents, got {documents_before}"
        )

    if chunks_before != 89:
        raise RuntimeError(
            f"Expected 89 knowledge chunks, got {chunks_before}"
        )

    if embeddings_before != 89:
        raise RuntimeError(
            f"Expected 89 embeddings, got {embeddings_before}"
        )

    print("DATABASE PRECONDITION: PASS")


    print("\n===== 2. INITIALIZE GROUNDED ANSWER SERVICE =====")

    service = GroundedAnswerService()

    print("GroundedAnswerService: PASS")


    print("\n===== 3. GROUNDING TEST SUITE =====")

    passed = 0

    for index, test_case in enumerate(TEST_CASES, start=1):

        name = test_case["name"]
        query = test_case["query"]
        expected_grounded = test_case["expected_grounded"]

        print(
            f"\n===== TEST {index}/{len(TEST_CASES)} — {name} ====="
        )

        print("Question:", query)

        result = service.answer(
            query=query,
            top_k=5,
        )

        print("Grounded:", result.grounded)
        print("Answer length:", len(result.answer))
        print("Sources returned:", len(result.sources))

        if not result.answer:
            raise RuntimeError(
                f"{name}: empty answer."
            )

        expected_sources = test_case["expected_sources"]

        if len(result.sources) != expected_sources:
            raise RuntimeError(
                f"{name}: expected {expected_sources} sources, "
                f"got {len(result.sources)}"
            )

        if expected_grounded and result.grounded is not True:
            raise RuntimeError(
                f"{name}: expected grounded answer."
            )

        if not expected_grounded and result.grounded is True:
            raise RuntimeError(
                f"{name}: expected rejected/ungrounded answer."
            )

        if not expected_grounded and result.grounded is not False:
            raise RuntimeError(
                f"{name}: expected grounded=False."
            )

        print("\nANSWER:")
        print(result.answer)

        print("\nSOURCES:")

        for source in result.sources:
            print(
                f"Rank {source.rank} | "
                f"Score {source.similarity_score:.6f} | "
                f"{source.title} | "
                f"Verified={source.is_verified}"
            )

        print(f"\n{name}: COMPLETED")

        passed += 1


    print("\n===== 4. GROUNDING BEHAVIOR SUMMARY =====")

    print("Tests executed:", len(TEST_CASES))
    print("Tests completed:", passed)

    if passed != len(TEST_CASES):
        raise RuntimeError(
            "Not all grounding tests completed."
        )

    print("GROUNDING TEST EXECUTION: PASS")


    print("\n===== 5. POST-TEST DATABASE STATE =====")

    documents_after = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_documents")
    ).scalar_one()

    chunks_after = db.execute(
        text("SELECT COUNT(*) FROM ai_knowledge_chunks")
    ).scalar_one()

    embeddings_after = db.execute(
        text("SELECT COUNT(*) FROM ai_embeddings")
    ).scalar_one()

    print("Knowledge documents:", documents_after)
    print("Knowledge chunks:", chunks_after)
    print("AI embeddings:", embeddings_after)

    if documents_after != documents_before:
        raise RuntimeError(
            "Knowledge document count changed."
        )

    if chunks_after != chunks_before:
        raise RuntimeError(
            "Knowledge chunk count changed."
        )

    if embeddings_after != embeddings_before:
        raise RuntimeError(
            "Embedding count changed."
        )

    print("MYSQL NO-MUTATION CHECK: PASS")


    print("\n===== STEP 8B-013R: PASS =====")

    print("Supported-question testing: PASS")
    print("Cross-site testing: PASS")
    print("Historical-question testing: PASS")
    print("Unsupported-question testing: COMPLETED")
    print("Unrelated-question testing: COMPLETED")
    print("Misleading-question testing: COMPLETED")
    print("MySQL no-mutation: PASS")

finally:

    if service is not None:
        service.close()

    db.close()
