"""Tests for the vector store."""
import pytest
from unittest.mock import MagicMock, patch

from adriacb_galtea.core.vector_store import LangChainVectorStore
from adriacb_galtea.core.base import Document

@pytest.fixture
def mock_embeddings():
    """Fixture to mock the embeddings model."""
    mock = MagicMock()
    mock.embed_query.return_value = [0.1, 0.2, 0.3]
    mock.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    return mock

@pytest.fixture
def mock_langchain_document():
    """Fixture to mock LangChain's Document."""
    mock = MagicMock()
    mock.page_content = "test content"
    mock.metadata = {"id": "1"}
    return mock

@pytest.fixture
def mock_inmemory_store():
    """Fixture to mock LangChain's InMemoryVectorStore."""
    with patch("langchain_core.vectorstores.InMemoryVectorStore") as mock_class:
        mock_instance = MagicMock()
        mock_instance.add_documents.return_value = None
        mock_instance.similarity_search_with_score.return_value = []
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def vector_store(mock_embeddings, mock_inmemory_store):
    """Fixture to create a LangChainVectorStore instance."""
    store = LangChainVectorStore(embeddings=mock_embeddings)
    store._store = mock_inmemory_store
    return store

def test_add_documents(vector_store, mock_inmemory_store):
    """Test adding documents to the vector store."""
    documents = [
        Document(id="1", content="doc1", metadata={"source": "test"}),
        Document(id="2", content="doc2", metadata={"source": "test"})
    ]
    
    vector_store.add_documents(documents)
    
    # Check that documents were stored
    assert "1" in vector_store._documents
    assert "2" in vector_store._documents
    assert vector_store._documents["1"] == documents[0]
    assert vector_store._documents["2"] == documents[1]
    
    # Check that LangChain store was called
    mock_inmemory_store.add_documents.assert_called_once()

def test_search(vector_store, mock_inmemory_store, mock_langchain_document):
    """Test searching the vector store."""
    # Add a document first
    doc = Document(id="1", content="test content", metadata={})
    vector_store._documents["1"] = doc
    mock_inmemory_store.similarity_search_with_score.return_value = [
        (mock_langchain_document, 0.8)
    ]
    
    results = vector_store.search("test query")
    
    # Check that search was called with correct parameters
    mock_inmemory_store.similarity_search_with_score.assert_called_once_with(
        "test query", k=5
    )
    
    # Check results
    assert len(results) == 1
    assert isinstance(results[0], dict)
    assert "document" in results[0]
    assert "score" in results[0]
    assert results[0]["document"] == doc
    assert results[0]["score"] == 0.8

def test_delete_document(vector_store):
    """Test deleting a document from the vector store."""
    # Add a document first
    doc = Document(id="1", content="test content", metadata={})
    vector_store._documents["1"] = doc
    
    # Delete the document
    vector_store.delete_document("1")
    
    # Check that document was removed
    assert "1" not in vector_store._documents 