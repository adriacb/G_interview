# Development Guide

## Setup Development Environment

### Prerequisites
- Python 3.9+
- uv package manager
- OpenAI API key

### Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
```bash
uv add .
```

### Environment Variables
Create a `.env` file with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
VECTOR_STORE_PATH=vector_store
API_HOST=0.0.0.0
API_PORT=8000
```

## Project Structure
```
adriacb_galtea/
├── src/
│   ├── adriacb_galtea/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── services/
│   │   │   └── run.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── base.py
│   │   │   ├── config.py
│   │   │   ├── config/
│   │   │   ├── document_processor.py
│   │   │   ├── embeddings.py
│   │   │   ├── graph.py
│   │   │   ├── langfuse_service.py
│   │   │   ├── state.py
│   │   │   ├── tools.py
│   │   │   └── vector_store.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── utils/
│   │   │   └── logging.py
│   │   ├── __init__.py
│   │   └── config.py
│   └── data/
├── tests/
├── data/
├── notebooks/
│   ├── api/
│   ├── development/
│   └── user-guide/
├── pyproject.toml
├── pytest.ini
├── .env.template
├── .python-version
├── .gitignore
├── plan.md
└── prd.md
```

## Development Workflow

### 1. Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all public functions and classes

### 2. Testing
- Write unit tests for all components
- Run tests before committing:
```bash
python -m pytest
```

### 3. Documentation
- Update API documentation when making changes
- Keep user guide up to date
- Document any new features

### 4. Version Control
- Create feature branches for new features
- Use descriptive commit messages
- Create pull requests for review

## Core Components

### Base Components
- `base.py`: Contains base classes and interfaces for the core functionality
- `state.py`: Manages application state and state transitions
- `config.py`: Core configuration settings and constants

### Document Processing
- `document_processor.py`: Handles document processing:
  - Converts documents to markdown
  - Extracts metadata
  - Splits content by headers
  - Limits chunks to 50 per document
- `tools.py`: Utility functions for document processing and manipulation

### Vector Storage and Embeddings
- `vector_store.py`: Manages document storage:
  - Uses ChromaDB for persistent storage
  - Handles embeddings and metadata
  - Provides semantic search functionality
- `embeddings.py`: Handles embedding generation and management:
  - Embedding model configuration
  - Batch processing
  - Caching and optimization

### Agent and Graph
- `agent.py`: Implements the agent functionality:
  - Agent configuration
  - Tool management
  - Response generation
- `graph.py`: Manages graph-based operations:
  - Graph construction
  - Node management
  - Edge handling

### Monitoring and Analytics
- `langfuse_service.py`: Integration with Langfuse:
  - Performance monitoring
  - Usage tracking
  - Analytics collection

### Configuration
- `config/`: Directory containing configuration files:
  - Settings management
  - Environment-specific configs
  - Feature flags

### API Layer
FastAPI-based REST API with endpoints for:
- Document injection (single and batch)
- Semantic search
- Error handling and logging

## Development Setup

### Environment
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all public functions and classes
- Keep functions focused and small

## Implementation Details

### Document Processing
1. Document is read and converted to markdown
2. Content is split by headers (H1-H4)
3. Each section is processed into chunks
4. Metadata is extracted and attached
5. Chunks are limited to 50 per document

### Vector Storage
1. Documents are stored in ChromaDB
2. Each chunk gets its own embedding
3. Metadata is preserved for search
4. Storage is persistent across sessions

### API Implementation
1. FastAPI handles routing and validation
2. Services manage business logic
3. Error handling is centralized
4. Logging is implemented throughout

## Testing

### Unit Tests
- Test each component independently
- Mock external dependencies
- Cover edge cases and error conditions

### Integration Tests
- Test component interactions
- Verify API endpoints
- Check data flow through the system

## Deployment

### Requirements
- Python 3.8+
- ChromaDB
- FastAPI
- Uvicorn

### Configuration
- Set up logging
- Configure ChromaDB path
- Set API host and port

## Contributing

### Workflow
1. Create a feature branch
2. Make changes
3. Run tests
4. Submit pull request

### Code Review
- Ensure tests pass
- Check code style
- Verify documentation
- Review error handling

## Troubleshooting

### Common Issues
1. ChromaDB connection errors
   - Check storage path
   - Verify permissions
   - Ensure ChromaDB is running

2. Document processing failures
   - Check file format
   - Verify document content
   - Review error logs

3. API issues
   - Check server status
   - Review request format
   - Check error responses

## Performance Considerations

### Document Processing
- Optimize chunk size
- Consider parallel processing
- Monitor memory usage

### Search
- Index optimization
- Query caching
- Result limiting

## Future Improvements
1. Add authentication
2. Implement rate limiting
3. Add more metadata fields
4. Improve search accuracy
5. Add monitoring and metrics 