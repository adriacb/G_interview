# User Guide

## Introduction
This guide explains how to use the document processing and search system. The system allows you to upload documents, process them into searchable chunks, and perform semantic searches across your document collection.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd adriacb_galtea
```

2. Install dependencies:
```bash
pip install -e .
```

3. Start the API server:
```bash
python -m adriacb_galtea.api.run
```

## Using the System

### Document Upload

#### Single Document
You can upload a single document using the `/inject` endpoint:

```bash
curl -X POST "http://localhost:8000/api/v1/inject" \
     -H "accept: application/json" \
     -F "file=@path/to/your/document.pdf" \
     -F "max_chunks=50"
```

#### Multiple Documents
To upload multiple documents at once, use the `/inject/batch` endpoint:

```bash
curl -X POST "http://localhost:8000/api/v1/inject/batch" \
     -H "accept: application/json" \
     -F "files=@document1.pdf" \
     -F "files=@document2.pdf" \
     -F "max_chunks=50"
```

### Searching Documents

Perform a semantic search across your documents:

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "Your search query", "k": 5}'
```

## Features

### Document Processing
- Automatic conversion of documents to markdown
- Header-based chunking for better context preservation
- Metadata extraction (filename, size, type)
- Configurable chunk size limit (default: 50 chunks per document)

### Search Capabilities
- Semantic search across all documents
- Relevance scoring for search results
- Metadata filtering and sorting
- Configurable number of results

## Best Practices

### Document Upload
1. Ensure documents are in a supported format (PDF, DOCX, etc.)
2. Keep document size reasonable (under 100MB recommended)
3. Use meaningful filenames for better organization
4. Consider the chunk limit when uploading large documents

### Search Tips
1. Use natural language queries
2. Be specific in your search terms
3. Use the `k` parameter to control the number of results
4. Check metadata for additional context

## Troubleshooting

### Common Issues

#### Document Upload Fails
- Check file format and size
- Ensure the API server is running
- Verify file permissions

#### Search Returns No Results
- Try different search terms
- Check if documents were successfully uploaded
- Verify the document content is searchable

#### Performance Issues
- Reduce the number of concurrent uploads
- Consider splitting large documents
- Check system resources

## Support
For additional help or to report issues, please contact the development team or create an issue in the repository. 