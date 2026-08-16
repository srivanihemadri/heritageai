from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.ai.generation import GroundedAnswerService


QUERY = "Tell me about the ancient Buddhist caves in Maharashtra."


db = SessionLocal()
service = None

try:

    print("===== 1. PRE-GENERATION DATABASE STATE =====")

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
            f"Expected 89 documents, got {documents_before}"
        )

    if chunks_before != 89:
        raise RuntimeError(
            f"Expected 89 chunks, got {chunks_before}"
        )

    if embeddings_before != 89:
        raise RuntimeError(
            f"Expected 89 embeddings, got {embeddings_before}"
        )

    print("DATABASE PRECONDITION: PASS")


    print("\n===== 2. INITIALIZE GROUNDED ANSWER SERVICE =====")

    service = GroundedAnswerService()

    print("GroundedAnswerService: PASS")


    print("\n===== 3. USER QUESTION =====")

    print("Question:", QUERY)


    print("\n===== 4. GENERATE GROUNDED ANSWER =====")

    result = service.answer(
        query=QUERY,
        top_k=5,
    )

    print("Generation request completed: YES")


    print("\n===== 5. ANSWER CONTRACT VALIDATION =====")

    if result.query != QUERY:
        raise RuntimeError("Returned query does not match input.")

    if not result.answer:
        raise RuntimeError("Gemini returned an empty answer.")

    if result.grounded is not True:
        raise RuntimeError("Expected grounded=True.")

    if len(result.sources) != 5:
        raise RuntimeError(
            f"Expected 5 sources, got {len(result.sources)}"
        )

    print("Query:", result.query)
    print("Answer length:", len(result.answer))
    print("Grounded:", result.grounded)
    print("Sources returned:", len(result.sources))
    print("ANSWER CONTRACT: PASS")


    print("\n===== 6. GENERATED ANSWER =====")

    print(result.answer)


    print("\n===== 7. EVIDENCE SOURCES =====")

    for source in result.sources:
        print(
            f"Rank {source.rank} | "
            f"Score {source.similarity_score:.6f} | "
            f"{source.title} | "
            f"Provenance={source.provenance_level} | "
            f"Verified={source.is_verified}"
        )


    print("\n===== 8. SOURCE CONTRACT VALIDATION =====")

    ranks = [source.rank for source in result.sources]

    if ranks != [1, 2, 3, 4, 5]:
        raise RuntimeError(
            f"Invalid source ranking: {ranks}"
        )

    for source in result.sources:

        if not source.chunk_id:
            raise RuntimeError("Missing chunk_id.")

        if not source.document_id:
            raise RuntimeError("Missing document_id.")

        if not source.title:
            raise RuntimeError("Missing title.")

        if not 0.0 <= source.similarity_score <= 1.0:
            raise RuntimeError(
                f"Invalid similarity score: {source.similarity_score}"
            )

        if not source.provenance_level:
            raise RuntimeError("Missing provenance level.")

    print("SOURCE CONTRACT: PASS")


    print("\n===== 9. GROUNDING SAFETY VALIDATION =====")

    answer_lower = result.answer.lower()

    if "similarity score" in answer_lower:
        raise RuntimeError(
            "Answer exposed internal similarity metadata."
        )

    if "similarity:" in answer_lower:
        raise RuntimeError(
            "Answer exposed internal similarity metadata."
        )

    print("Internal retrieval metadata hidden: PASS")


    print("\n===== 10. POST-GENERATION DATABASE STATE =====")

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


    print("\n===== STEP 8B-013Q-D: PASS =====")

    print("Grounded answer generation: PASS")
    print("Gemini generation: PASS")
    print("Answer contract: PASS")
    print("Source contract: PASS")
    print("Grounding safety: PASS")
    print("MySQL no-mutation: PASS")

finally:

    if service is not None:
        service.close()

    db.close()
