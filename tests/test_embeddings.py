"""Tests for the embedding models."""
import os
import pytest
from unittest.mock import MagicMock, patch

from adriacb_galtea.core.embeddings import OpenAIEmbeddingModel
from adriacb_galtea.core.base import Document

@pytest.fixture(autouse=True)
def mock_openai_api_key():
    """Fixture to mock the OpenAI API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield

@pytest.fixture
def mock_openai_embeddings():
    """Fixture to mock OpenAIEmbeddings."""
    with patch("langchain_openai.OpenAIEmbeddings") as mock_class:
        mock_instance = MagicMock()
        mock_instance.embed_query.return_value = [0.1, 0.2, 0.3]
        mock_instance.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_instance.model = "test-model"
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def embedding_model(mock_openai_embeddings):
    """Fixture to create an OpenAIEmbeddingModel instance."""
    with patch("openai.OpenAI"):  # Mock the OpenAI client
        model = OpenAIEmbeddingModel()
        # Mock the internal methods to avoid actual API calls
        model._model = mock_openai_embeddings
        return model

def test_embedding_model_initialization():
    """Test that the embedding model is initialized correctly."""
    with patch("openai.OpenAI"):  # Mock the OpenAI client
        model = OpenAIEmbeddingModel(model_name="test-model")
        assert model._model.model == "test-model"

def test_embed_text(embedding_model, mock_openai_embeddings):
    """Test embedding a single text."""
    text = "test text"
    result = embedding_model.embed_text(text)
    
    mock_openai_embeddings.embed_query.assert_called_once_with(text)
    assert result == [0.1, 0.2, 0.3]

def test_embed_documents(embedding_model, mock_openai_embeddings):
    """Test embedding multiple documents."""
    documents = [
        Document(id="1", content="doc1", metadata={}),
        Document(id="2", content="doc2", metadata={})
    ]
    
    result = embedding_model.embed_documents(documents)
    
    mock_openai_embeddings.embed_documents.assert_called_once_with(["doc1", "doc2"])
    assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]] 