from langchain_community.graphs.neo4j_graph import Neo4jGraph

class GraphStore:
    def __init__(self) -> None:
        self.graph = Neo4jGraph()

    def close(self) -> None:
        self.graph._driver.close()

    def __enter__(self) -> 'GraphStore':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def get_relation_embeddings_with_targets(self, entities):
        condition = [f"(e:{entity_type} AND e.id = '{id}')" for id, entity_type in entities]
        
        where = " OR ".join(condition)

        query = f"""
        MATCH (e)-[r]->(t)
        WHERE ({where})
        AND NOT type(r) IN ['EXTRACTED_FROM']
        AND NOT t:DocumentChunk
        RETURN r.embedding AS embedding, t.id AS target_id, labels(t) as target_labels
        """

        result = self.graph.query(query)

        embeddings = [record['embedding'] for record in result if record['embedding'] is not None]
        targets = [(record['target_id'], record['target_labels'][0]) for record in result]

        return embeddings, targets
    
    def get_most_connected_chunks(self, entities, k):
        condition = []

        for entity_id, entity_type in entities:
            condition.append(f"(e:{entity_type} AND e.id = '{entity_id}')")

        where = " OR ".join(condition)

        query = f"""
        MATCH (e)-[:EXTRACTED_FROM]->(d:DocumentChunk)
        WHERE {where}
        WITH d.content AS content, d.id AS chunk_id, COUNT(d) AS num_connections
        RETURN content, chunk_id, num_connections
        ORDER BY num_connections DESC
        LIMIT {k}
        """

        result = self.graph.query(query)

        return [chunk.get('content') for chunk in result], [chunk.get('chunk_id') for chunk in result]