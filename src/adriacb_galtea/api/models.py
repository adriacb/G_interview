"""API models for the RAG application."""
from pydantic import BaseModel
from typing import List, Optional


class Query(BaseModel):
    """Query model."""
    question: str


class Ingest(BaseModel):
    """Ingest model."""
    pdf_path: str


class Response(BaseModel):
    """Response model."""
    answer: str


class QueryRequest(BaseModel):
    """Request model for querying the RAG system."""
    query: str
    context: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for querying the RAG system."""
    answer: str
    sources: List[str] = []


class DocumentInjectionResponse(BaseModel):
    """Response model for document injection."""
    doc_id: str
    status: str = "success"


class DocumentsInjectionResponse(BaseModel):
    """Response model for multiple document injection."""
    doc_ids: List[str]
    status: str = "success"


class DocumentDeletionResponse(BaseModel):
    """Response model for document deletion."""
    doc_id: str
    status: str = "success"
    deleted: bool 