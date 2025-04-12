# RAG Application for PDF Question Answering

A powerful RAG (Retrieval-Augmented Generation) application that processes PDF documents, stores them in a vector database, and provides a REST API for querying the content.

## Features

- PDF document processing with Docling
- Vector storage using ChromaDB
- FastAPI-based REST API
- LangGraph orchestration for advanced query processing
- Docker support for easy deployment

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- UV package manager

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/adriacb_galtea.git
cd adriacb_galtea
```

2. Create and configure your `.env` file:
```bash
cp .env.template .env
# Edit .env and add your OpenAI API key
```

3. Build and start the services:
```bash
docker-compose up --build
```

This will start:
- API service at `http://localhost:8000`
- LangGraph studio at `https://smith.langchain.com/studio/?baseUrl=http://localhost:2024`

### Manual Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv sync
```

3. Run the API:
```bash
python -m adriacb_galtea.api.run
```

## API Endpoints

### Document Injection

```http
POST /api/v1/inject
```
Inject a single document into the vector store.

```http
POST /api/v1/inject/batch
```
Inject multiple documents into the vector store.

### Query

```http
POST /api/v1/query
```
Query the vector store with a question.

## Project Structure

```
adriacb_galtea/
├── src/
│   └── adriacb_galtea/
│       ├── api/
│       │   ├── routes.py
│       │   └── run.py
│       ├── core/
│       │   ├── document_processor.py
│       │   └── vector_store.py
│       └── config/
├── tests/
├── notebooks/
├── data/
└── docker-compose.yml
```

## Configuration

Key settings in `.env`:
```
# OpenAI settings
OPENAI_API_KEY=your_openai_api_key_here

# Vector store settings
VECTOR_STORE_PATH=vector_store

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# Logging settings
LOG_LEVEL=INFO
```

## Development

### Running Tests
```bash
pytest
```

## License

MIT License

## Contact

For support or questions, please open an issue in the repository.
