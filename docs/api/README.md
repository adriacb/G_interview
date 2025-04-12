# API Documentation

## Overview
The API provides endpoints for document processing, storage, and semantic search using ChromaDB as the vector store.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API does not require authentication. This will be implemented in future versions.

## Endpoints

### Query Documents

```http
POST /query
```

Process a query using the RAG system with streaming response.

**Request Body:**
```json
{
    "query": "Your question about the documents"
}
```

**Response:**
Server-Sent Events (SSE) stream with the following format:
```json
{
    "answer": "The answer to your question",
    "sources": [
        {
            "content": "Relevant document content",
            "metadata": {
                "source_file": "document.pdf",
                "headers": "Section > Subsection"
            }
        }
    ]
}
```

### Inject Document

```http
POST /inject
```

Inject a single document into the vector store.

**Request:**
- Content-Type: `multipart/form-data`
- File: PDF document to inject

**Response:**
```json
{
    "success": true,
    "message": "Document processed successfully",
    "chunks_processed": 42
}
```

### Inject Multiple Documents

```http
POST /inject/batch
```

Inject multiple documents into the vector store.

**Request:**
- Content-Type: `multipart/form-data`
- Files: Multiple PDF documents to inject

**Response:**
```json
[
    {
        "success": true,
        "message": "Document processed successfully",
        "chunks_processed": 42
    },
    {
        "success": false,
        "message": "Error processing document",
        "chunks_processed": 0
    }
]
```

### Delete Document

```http
DELETE /documents/{doc_id}
```

Delete a document from the vector store.

**Parameters:**
- `doc_id`: ID of the document to delete

**Response:**
```json
{
    "success": true
}
```

## Error Handling

All endpoints may return the following error responses:

```json
{
    "detail": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting
Currently, there are no rate limits implemented. This will be added in future versions.

## Notes
- Documents are processed using the DoclingProcessor, which splits content by headers and creates chunks
- Each document is limited to 50 chunks by default
- The vector store uses ChromaDB with persistent storage
- All operations are logged for debugging and monitoring
- The API uses FastAPI and supports automatic OpenAPI documentation at `/docs`
- All endpoints are prefixed with `/api/v1`
- The query endpoint uses Server-Sent Events for streaming responses
- Document injection supports PDF files
- Error responses include detailed messages for debugging 