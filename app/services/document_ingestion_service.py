import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from app.services.chunk_service import chunk_text

class DocumentIngestionService:

    def __init__(
        self,
        qdrant_client: QdrantClient,
        embedding_model: SentenceTransformer,
        collection_name: str
    ):
        self.qdrant_client = qdrant_client
        self.embedding_model = embedding_model
        self.collection_name = collection_name

        self.embedding_dimension = (
            self.embedding_model.get_embedding_dimension()
        )

        self._create_collection()

    def _create_collection(self):

        if not self.qdrant_client.collection_exists(
            self.collection_name
        ):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_dimension,
                    distance=models.Distance.COSINE
                )
            )

    def ingest_document(
        self,
        document_id: str,
        document_text: str,
        metadata: dict | None = None
    ):

        if not document_text.strip():
            raise ValueError("Document text cannot be empty")

        chunks = chunk_text(
            document_text,
            chunk_size=40,
            overlap=10
        )
      
        embeddings = self.embedding_model.encode(
            inputs=chunks,
            convert_to_numpy=True
            )

        points = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            points.append(
                models.PointStruct(
                    id=uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"{document_id}:{index}"
                    ),
                    vector=embedding.tolist(),
                    payload={
                        "document_id": document_id,
                        "chunk_index": index,
                        "text": chunk,
                        **(metadata or {})
                    }
                )
            )

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return {
            "document_id": document_id,
            "total_chunks": len(chunks),
            "status": "ingested"
        }
