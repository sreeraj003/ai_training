
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient, models

# # 1. Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # 2. Our documents
# documents = [
#     "Python is a programming language.",
#     "FastAPI is used to build backend APIs.",
#     "Football is a popular sport.",
#     "React is a JavaScript library for frontend development."
# ]

# # 3. Generate document embeddings
# embeddings = model.encode(documents)

# # 4. Connect to local Qdrant database
# client = QdrantClient(path="./qdrant_data")

# collection_name = "opspilot_knowledge"

# # 5. Create collection if it doesn't exist
# if not client.collection_exists(collection_name):
#     client.create_collection(
#         collection_name=collection_name,
#         vectors_config=models.VectorParams(
#             size=384,
#             distance=models.Distance.COSINE
#         )
#     )

# # 6. Insert documents and vectors
# points = []

# for index, (document, embedding) in enumerate(
#     zip(documents, embeddings)
# ):
#     points.append(
#         models.PointStruct(
#             id=index + 1,
#             vector=embedding.tolist(),
#             payload={
#                 "text": document,
#                 "category": "general"
#             }
#         )
#     )

# client.upsert(
#     collection_name=collection_name,
#     points=points
# )

# print("Documents inserted successfully!")

# # 7. User query
# query = "How can I develop server-side applications?"

# query_embedding = model.encode(query)

# # 8. Search Qdrant
# results = client.query_points(
#     collection_name=collection_name,
#     query=query_embedding.tolist(),
#     limit=2,
#     with_payload=True
# )

# # 9. Display results
# for point in results.points:
#     print(
#         f"Score: {point.score:.4f} | "
#         f"Document: {point.payload['text']}"
#     )

# client.close()
# from app.services.chunk_service import chunk_text

# text = """
# FastAPI is a modern Python web framework.
# It supports asynchronous programming.
# It is commonly used for building APIs.
# Python is also popular in AI engineering.
# """

# chunks = chunk_text(
#     text,
#     chunk_size=10,
#     overlap=3
# )

# for index, chunk in enumerate(chunks):
#     print(f"\nChunk {index + 1}:")
#     print(chunk)


from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from app.services.retrieval_service import RetrievalService
import asyncio
from app.services.rag_service import RAGService
from app.services.document_ingestion_service import (
    DocumentIngestionService
)

# Load model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local Qdrant
client = QdrantClient(path="./qdrant_data")

# Initialise ingestion service
ingestion_service = DocumentIngestionService(
    qdrant_client=client,
    embedding_model=embedding_model,
    collection_name="opspilot_knowledge"
)

document_text = """
FastAPI is a modern Python framework for building APIs.

FastAPI supports asynchronous programming through Python's async and await
syntax. Developers can define asynchronous route handlers using async def.
When an asynchronous route handler awaits an I/O operation, such as a
database request or external API call, the event loop can execute other
tasks while waiting for that operation to complete.

FastAPI uses Pydantic for request validation.

FastAPI applications can integrate with PostgreSQL,
Redis and external AI services.
"""

try:
    result = ingestion_service.ingest_document(
        document_id="python_backend_001",
        document_text=document_text,
        metadata={"source": "test"}
    )

    print(result)
    
    retrieval_service = RetrievalService(
    qdrant_client=client,
    embedding_model=embedding_model,
    collection_name="opspilot_knowledge"
)

    query = "How does FastAPI handle asynchronous programming?"

    results = retrieval_service.retrieve(
        query=query,
        top_k=3,
    )

    for result in results:
        print("\nScore:", result["score"])
        print("Document:", result["document_id"])
        print("Content:", result["text"])
    rag_service = RAGService(
        retrieval_service=retrieval_service
    )

    async def test_rag():

        response = await rag_service.generate_answer(
        query="How does FastAPI handle asynchronous programming?",
        document_id="python_backend_001",
        top_k=3
    )

        print("\nAI ANSWER:")
        print(response["answer"])

        print("\nCITATIONS:")
        for source in response["sources"]:
            print(source)


    asyncio.run(test_rag())

finally:
    client.close()


