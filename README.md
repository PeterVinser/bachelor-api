# bachelor-api

This is an API for bachelor's thesis app. It focuces on querying the RAG service.

The API has one main endpoint:
- /api/query/

## Query

### Request:

Header:

- X-Retrieval-Type:
    - 0 - vector db based retrieval
    - 1 - graph based retrieval
    - 2 - fusion retrieval
- X-OpenAI-Api-Key
- X-Weaviate-Key
- X-Neo4j-Password
- X-Noe4j-Uri
- X-Temperature

Body:

{
    "question": <question>
}

### Response

Body:

{
    "answer": <system's answer>,
    "context": [
        {
            "chunkId": <id of used chunk>,
            "chunkContent": <text content of used chunk>
        }
    ]
}

## Environment variables
- WEAVIATE_HOST
- NOE4J_USERNAME