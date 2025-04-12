"""Test the document injection pipeline."""
import pytest
from fastapi import UploadFile
from io import BytesIO

from src.adriacb_galtea.core.vector_store import LangChainVectorStore
from src.adriacb_galtea.core.embeddings import get_embeddings
from src.adriacb_galtea.api.services.injection_service import InjectionService


@pytest.fixture
def embeddings():
    """Create an embeddings model."""
    return get_embeddings()


@pytest.fixture
def vector_store(embeddings):
    """Create a vector store instance."""
    return LangChainVectorStore(embeddings=embeddings)


@pytest.fixture
def injection_service(vector_store):
    """Create an injection service instance."""
    return InjectionService(vector_store)


@pytest.fixture
def test_document():
    """Create a test document."""
    content = "This is a test document for the injection pipeline."
    return UploadFile(
        file=BytesIO(content.encode('utf-8')),
        filename="test.txt"
    )


@pytest.mark.asyncio
async def test_inject_document(injection_service, test_document):
    """Test injecting a single document."""
    # Inject document
    doc_id = await injection_service.inject_document(test_document)
    
    # Verify document was stored
    assert doc_id is not None
    assert len(doc_id) > 0
    
    # Clean up
    await injection_service.delete_document(doc_id)


@pytest.mark.asyncio
async def test_inject_documents(injection_service, test_document):
    """Test injecting multiple documents."""
    # Create multiple test documents
    docs = [
        UploadFile(
            file=BytesIO(f"Test document {i}".encode('utf-8')),
            filename=f"test_{i}.txt"
        )
        for i in range(3)
    ]
    
    # Inject documents
    doc_ids = await injection_service.inject_documents(docs)
    
    # Verify documents were stored
    assert len(doc_ids) == 3
    assert all(len(doc_id) > 0 for doc_id in doc_ids)
    
    # Clean up
    for doc_id in doc_ids:
        await injection_service.delete_document(doc_id)


@pytest.mark.asyncio
async def test_delete_document(injection_service, test_document):
    """Test deleting a document."""
    # Inject document
    doc_id = await injection_service.inject_document(test_document)
    
    # Delete document
    success = await injection_service.delete_document(doc_id)
    
    # Verify deletion
    assert success is True 