# bachelor-api

This is an API for bachelor's thesis app.

The API has four endpoints that together form a CRUD pattern:
- /api/query/
- /api/add/
- /api/update/
- /api/delete/

## Query

### Request:

Header:

- X-Retrieval-Type:
    - 0 - vector db based retrieval
    - 1 - graph based retrieval
    - 2 - fusion retrieval

Body:

{
    "question": <user question>
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

## Add

Adds a given document for all retrieval types (vector-db, graph and fusion based)

### Request:

Body:

{
    "documentName": <document name>,
    "documentContent": <document content>
}

### Response

Body:

{
    "resultMessage": <result of addition>
}

## Update

This is a placeholder. This component may not be used in the end.

## Delete

Deletes all documents with specified name.

### Request:

Body:

{
    "documentName": <document name>
}

### Response

Body:

{
    "resultMessage": <result of deletion>
}