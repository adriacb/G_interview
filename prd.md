# Product Requirements Document (PRD) for Galtea RAG Application

## Overview
Galtea is a Retrieval-Augmented Generation (RAG) application that provides intelligent responses by combining a language model with a vector store of documents. The application uses a React agent pattern to handle conversation flow and tool execution.

## Core Components

### 1. State Management
- **RAGState**: A TypedDict that maintains the conversation state including:
  - Messages: List of conversation messages
  - Documents: Retrieved documents for context
  - Vector Store: Reference to the vector store for document retrieval

### 2. Graph Architecture
- **React Agent**: Uses LangGraph's prebuilt React agent pattern
- **Tools**: Custom tools for document retrieval and response generation
- **Model**: GPT-4 for response generation

### 3. Vector Store Integration
- Document storage and retrieval
- Semantic search capabilities
- Document preprocessing and chunking

## Technical Implementation

### State Definition
```python
class RAGState(TypedDict):
    messages: List[BaseMessage]
    documents: List[Document]
    vector_store: VectorStore
```

### Graph Structure
The application uses a React agent pattern with the following components:
- Prebuilt React agent from LangGraph
- Custom tools for RAG-specific operations
- GPT-4 model for response generation

### Tools
1. Document Retrieval Tool
   - Queries the vector store
   - Returns relevant documents
   - Updates state with retrieved documents

2. Response Generation Tool
   - Uses retrieved documents as context
   - Generates responses using GPT-4
   - Updates conversation state

## Development Phases

### Phase 1: Core Implementation
- [x] State management setup
- [x] Graph architecture with React agent
- [ ] Vector store integration
- [ ] Tool implementation

### Phase 2: Testing & Optimization
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Error handling

### Phase 3: Deployment
- [ ] Documentation
- [ ] Deployment pipeline
- [ ] Monitoring setup
- [ ] User feedback collection

## Project Structure
```
adriacb_galtea/
├── src/
│   └── adriacb_galtea/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── document_processor.py
│       │   ├── vector_store.py
│       │   └── agent.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── models.py
│       └── utils/
│           ├── __init__.py
│           └── logging.py
├── tests/
│   ├── __init__.py
│   ├── test_document_processor.py
│   ├── test_vector_store.py
│   ├── test_agent.py
│   └── test_api.py
├── docs/
│   ├── api/
│   ├── development/
│   └── user-guide/
├── .env.template
├── pyproject.toml
└── README.md
```

## Clean Code Principles
1. **Single Responsibility Principle**
   - Each module and class has a single, well-defined purpose
   - Clear separation between document processing, vector storage, and agent logic

2. **Dependency Injection**
   - Components are loosely coupled
   - Dependencies are injected rather than hardcoded
   - Easy to swap implementations (e.g., different vector stores)

3. **Interface Segregation**
   - Clear interfaces for each component
   - Minimal dependencies between components
   - Easy to test and mock

4. **Error Handling**
   - Consistent error handling strategy
   - Clear error messages and logging
   - Graceful degradation

5. **Testing**
   - Comprehensive test coverage
   - Unit tests for each component
   - Integration tests for the full system

## Problem Statement
Users need a simple way to:
1. Upload and process PDF documents
2. Ask questions about the content of these documents
3. Get accurate, context-aware answers based on the document content

## Solution
A RAG-based application that:
1. Processes PDFs using Docling (state-of-the-art PDF processing)
2. Stores document embeddings in a vector store
3. Uses a ReAct agent to intelligently answer questions
4. Provides a simple API interface for interaction

## Technical Architecture

### Components
1. **PDF Processing Layer**
   - Uses Docling for PDF to text conversion
   - Handles various PDF formats and layouts
   - Preserves document structure and formatting

2. **Vector Store Layer**
   - FAISS for efficient similarity search
   - Stores document embeddings
   - Enables semantic search capabilities

3. **Agent Layer**
   - LangGraph ReAct agent
   - OpenAI LLM integration
   - Tool-based document retrieval

4. **API Layer**
   - FastAPI for REST endpoints
   - Async processing
   - Error handling and validation

### Data Flow
1. PDF Upload → Docling Processing → Text Extraction
2. Text → Embeddings → Vector Store
3. Question → ReAct Agent → Document Retrieval → Answer Generation

## Features

### Core Features
1. **Document Ingestion**
   - PDF upload and processing
   - Text extraction and cleaning
   - Vector store population

2. **Question Answering**
   - Natural language queries
   - Context-aware responses
   - Document-based evidence

3. **API Interface**
   - RESTful endpoints
   - JSON request/response format
   - Error handling

### Technical Requirements
1. Python 3.9+
2. OpenAI API access
3. Sufficient storage for vector store
4. Memory for document processing

## Success Metrics
1. **Accuracy**
   - Question answering accuracy
   - Document retrieval relevance

2. **Performance**
   - Response time
   - Document processing speed
   - API latency

3. **Reliability**
   - System uptime
   - Error rate
   - Recovery time

## Limitations
1. PDF processing quality depends on document structure
2. Response quality depends on OpenAI API
3. Vector store size limitations
4. Processing time for large documents

## Future Enhancements
1. Support for additional document formats
2. Batch processing capabilities
3. User authentication and document management
4. Customizable chunking strategies
5. Advanced evaluation metrics 