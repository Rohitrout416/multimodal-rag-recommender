from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from typing import List, Dict, Any, Optional

class VectorService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
        self.client = QdrantClient(url=self.qdrant_url)
        self.collection_name = "products"
        self.vector_size = 768  # Gemini embedding-001 size

    def ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                print(f"Creating collection '{self.collection_name}'...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                print("Collection created.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            print(f"Error checking/creating collection: {e}")

    def upsert_products(self, products: List[Dict[str, Any]], embeddings: List[List[float]]):
        points = []
        for i, (product, embedding) in enumerate(zip(products, embeddings)):
            points.append(models.PointStruct(
                id=i,  # Using simple integer IDs for seed data, usage uuid in prod
                vector=embedding,
                payload=product
            ))
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Upserted {len(points)} products.")
        except Exception as e:
            print(f"Error upserting points: {e}")

    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return [hit.payload for hit in results]
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []

vector_service = VectorService()
