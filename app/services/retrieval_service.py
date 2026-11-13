
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models


class RetrievalService:

    def __init__(
        self,
        qdrant_client: QdrantClient,
        embedding_model: SentenceTransformer,
        collection_name: str
    ):
        self.qdrant_client = qdrant_client
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        document_id: str | None = None,
    ):
        similarity_threshold: float = 0.5

        if not query.strip():
            raise ValueError("Query cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            inputs=query,
            convert_to_numpy=True
        )

        # Build optional document filter
        query_filter = None

        if document_id:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )

        # Search Qdrant
        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            query_filter=query_filter,
            limit=top_k,
            with_payload=True
        )

        # Extract results
        retrieved_chunks = []

        for point in results.points:
            if point.score < similarity_threshold:
                    continue

            payload = point.payload or {}

            retrieved_chunks.append({
                "document_id": payload.get("document_id"),
                "chunk_index": payload.get("chunk_index"),
                "text": payload.get("text"),
                "score": point.score,
                "metadata": payload
            })

        return retrieved_chunks
