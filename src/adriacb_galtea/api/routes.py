"""API routes for the RAG application."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from typing import List


from ..core.graph import create_graph
from ..core.langfuse_service import get_langfuse_callback
from ..config.settings import settings
from ..utils.logging import get_logger
from .models import (
    QueryRequest,
    DocumentDeletionResponse
)
from .services.injection_service import InjectionService
from .services.graph_service import graph
from ..core.vector_store import ChromaVectorStore, get_vector_store

logger = get_logger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str

async def stream_response(graph, query: str):
    """Stream the response from the graph."""
    try:
        # Get Langfuse callback handler
        langfuse_handler = get_langfuse_callback(settings)
        
        # Stream the response with Langfuse monitoring
        async for chunk in graph.astream(
            {"messages": [("user", query)]},
            config={"callbacks": [langfuse_handler]} if langfuse_handler else {}
        ):
            if "messages" in chunk and chunk["messages"]:
                last_message = chunk["messages"][-1]
                if hasattr(last_message, "content"):
                    yield f"data: {json.dumps({'answer': last_message.content, 'sources': chunk.get('sources', [])})}\n\n"
    except Exception as e:
        logger.error("Error streaming response", exc_info=e)
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@router.post("/query")
async def query(request: QueryRequest):
    """Process a query using the RAG system with streaming response.
    
    Args:
        request: Query request containing the user's question
        
    Returns:
        StreamingResponse with answer and sources
    """
    try:
        return StreamingResponse(
            stream_response(graph, request.query),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error("Error processing query", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e))

def get_vector_store() -> ChromaVectorStore:
    """Get the vector store instance."""
    return get_vector_store()

def get_injection_service() -> InjectionService:
    """Get the injection service instance."""
    return InjectionService()

@router.post("/inject")
async def inject_document(
    file: UploadFile = File(...),
    service: InjectionService = Depends(get_injection_service)
) -> dict:
    """Inject a document into the vector store.
    
    Args:
        file: The document file to inject
        service: Injection service instance
        
    Returns:
        Dictionary containing injection status
    """
    try:
        # Save file temporarily
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            temp_path = temp_file.name

        try:
            # Process and inject the document
            result = service.inject_document(temp_path)
            return result
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except Exception as e:
        logger.error("Error injecting document", exc_info=e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inject/batch")
async def inject_documents(
    files: List[UploadFile] = File(...),
    service: InjectionService = Depends(get_injection_service)
) -> List[dict]:
    """Inject multiple documents into the vector store.
    
    Args:
        files: List of document files to inject
        service: Injection service instance
        
    Returns:
        List of injection results
    """
    return await service.inject_documents(files)

@router.delete("/documents/{doc_id}", response_model=DocumentDeletionResponse)
async def delete_document(
    doc_id: str,
    service: InjectionService = Depends(get_injection_service)
):
    """Delete a document from the vector store.
    
    Args:
        doc_id: ID of the document to delete
        service: Injection service instance
        
    Returns:
        Deletion status
    """
    success = await service.delete_document(doc_id)
    return DocumentDeletionResponse(success=success) 