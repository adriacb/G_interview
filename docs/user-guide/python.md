# Python User Guide

## Installation

```bash
pip install adriacb_galtea
```

## Basic Usage

### Document Processing

```python
from adriacb_galtea.core import DoclingProcessor

# Initialize the processor
processor = DoclingProcessor()

# Process a document
result = processor.process_document("path/to/your/document.pdf")

# Access the processed content
print(f"Processed content: {result['content']}")
print(f"Metadata: {result['metadata']}")
print(f"Number of chunks: {len(result['chunks'])}")
```

### Vector Store

```python
from adriacb_galtea.core import ChromaVectorStore, get_vector_store

# Get the vector store instance
vector_store = get_vector_store()

# Add documents
vector_store.add_documents([
    {
        "content": "Your document content",
        "metadata": {"source": "document1.pdf"}
    }
])

# Search documents
results = vector_store.search("Your search query", k=5)
for result in results:
    print(f"Content: {result['content']}")
    print(f"Score: {result['score']}")
    print(f"Metadata: {result['metadata']}")
```

### Document Injection Service

```python
from adriacb_galtea.api.services import InjectionService

# Initialize the injection service
service = InjectionService()

# Inject a document
result = service.inject_document("path/to/document.pdf", max_chunks=50)
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
print(f"Chunks processed: {result['chunks_processed']}")

# Delete a document
success = service.delete_document("document_id")
print(f"Deletion successful: {success}")
```

### API Usage

```python
import requests

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

# Inject a document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/inject", files=files)
    print(response.json())

# Query the system
response = requests.post(
    f"{BASE_URL}/query",
    json={"query": "Your question about the documents"}
)
print(response.json())
```

## Advanced Usage

### Custom Configuration

```python
from adriacb_galtea.config import Settings

# Create custom settings
settings = Settings(
    VECTOR_STORE_PATH="custom/path/to/vector/store",
    API_HOST="0.0.0.0",
    API_PORT=8000,
    LOG_LEVEL="DEBUG"
)
```

### Batch Processing

```python
from adriacb_galtea.api.services import InjectionService
from pathlib import Path

service = InjectionService()
documents_dir = Path("path/to/documents")

# Process all documents in a directory
for doc_path in documents_dir.glob("*.pdf"):
    try:
        result = service.inject_document(doc_path)
        print(f"Processed {doc_path.name}: {result['message']}")
    except Exception as e:
        print(f"Error processing {doc_path.name}: {e}")
```

### Error Handling

```python
from adriacb_galtea.api.services import InjectionService
from fastapi import HTTPException

service = InjectionService()

try:
    result = service.inject_document("path/to/document.pdf")
    if not result["success"]:
        print(f"Processing failed: {result['message']}")
except HTTPException as e:
    print(f"HTTP error: {e.detail}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Resource Management**
   ```python
   # Use context managers for file operations
   with open("document.pdf", "rb") as f:
       service.inject_document(f.name)
   ```

2. **Batch Processing**
   ```python
   # Process documents in batches
   batch_size = 10
   documents = list(Path("documents").glob("*.pdf"))
   for i in range(0, len(documents), batch_size):
       batch = documents[i:i + batch_size]
       for doc in batch:
           service.inject_document(doc)
   ```

3. **Error Handling**
   ```python
   # Implement comprehensive error handling
   try:
       result = service.inject_document(doc_path)
       if not result["success"]:
           print(f"Processing failed: {result['message']}")
   except Exception as e:
       print(f"Error: {e}")
   ```

4. **Configuration Management**
   ```python
   # Use environment variables for configuration
   import os
   from adriacb_galtea.config import Settings
   
   settings = Settings(
       VECTOR_STORE_PATH=os.getenv("VECTOR_STORE_PATH", "vector_store"),
       API_PORT=int(os.getenv("API_PORT", "8000"))
   )
   ```

## Examples

### Complete Document Processing Pipeline

```python
from adriacb_galtea.api.services import InjectionService
from pathlib import Path

def process_and_store_documents(doc_path: Path, max_chunks: int = 50):
    # Initialize the injection service
    service = InjectionService()
    
    try:
        # Process and inject document
        result = service.inject_document(doc_path, max_chunks=max_chunks)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "chunks_processed": result["chunks_processed"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Usage
result = process_and_store_documents(Path("document.pdf"))
print(result)
```

### Semantic Search Implementation

```python
from adriacb_galtea.core import get_vector_store

def search_documents(query: str, k: int = 5):
    vector_store = get_vector_store()
    
    try:
        results = vector_store.search(query, k=k)
        return {
            "success": True,
            "results": [
                {
                    "content": r["content"],
                    "score": r["score"],
                    "metadata": r["metadata"]
                }
                for r in results
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Usage
results = search_documents("Your search query")
print(results)
```

## Troubleshooting

### Common Issues

1. **Document Processing Errors**
   ```python
   # Check document format and content
   service = InjectionService()
   try:
       result = service.inject_document("document.pdf")
       if not result["success"]:
           print(f"Check if document is valid PDF: {result['message']}")
   except Exception as e:
       print(f"Error: {e}")
   ```

2. **Vector Store Connection Issues**
   ```python
   # Verify vector store connection
   vector_store = get_vector_store()
   try:
       results = vector_store.search("test query", k=1)
       print("Vector store connection successful")
   except Exception as e:
       print(f"Vector store connection failed: {e}")
   ```

3. **Memory Issues**
   ```python
   # Monitor memory usage
   import psutil
   process = psutil.Process()
   print(f"Memory usage: {process.memory_info().rss / 1024 / 1024} MB")
   ```

## Support

For additional help:
1. Check the [API documentation](../api/README.md)
2. Review the [development guide](../development/README.md)
3. Contact the development team 