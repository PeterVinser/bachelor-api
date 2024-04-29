# bachelor-api

This is an API for bachelor's thesis app.

## Request:

Header:

- X-Retrieval-Type:
    - 0 - vector db based retrieval
    - 1 - graph based retrieval
    - 2 - fusion retrieval

Body:

{
    "question": <user question>
}

## Response

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