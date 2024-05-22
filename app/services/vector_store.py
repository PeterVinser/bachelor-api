import weaviate
import os

class VectorStore:
    def __init__(self) -> None:
        self.client = weaviate.connect_to_wcs(
            cluster_url=os.getenv('WEAVIATE_HOST'),
            auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_READONLY_KEY')),
            headers={
                'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
            }
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> 'VectorStore':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def retrieve_chunks_content(self, question, k):
        collection = self.client.collections.get("BachelorDocumentChunk")
        
        response = collection.query.hybrid(
            query=question, alpha=0.6, limit=k
        )

        objects = response.objects

        return [chunk.properties.get("content") for chunk in objects], [str(chunk.uuid) for chunk in objects]
    
    def retrieve_entities(self, question, k):
        collection = self.client.collections.get("BachelorEntity")

        response = collection.query.hybrid(
            query=question, alpha=0.6, limit=k
        )

        entities = []

        for entity in response.objects:
            id, entity_type = entity.properties.get("entityId"), entity.properties.get("entityType")
            entities.append((id, entity_type))

        return entities