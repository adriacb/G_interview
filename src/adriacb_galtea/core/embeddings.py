"""Embeddings module for the RAG application."""
from typing import Optional, ClassVar

from langchain_openai import OpenAIEmbeddings

from ..config.settings import settings

class OpenAIEmbeddingModel:
    """OpenAI embedding model implementation."""
    
    _instance: ClassVar[Optional["OpenAIEmbeddingModel"]] = None
    
    @classmethod
    def get_instance(cls) -> "OpenAIEmbeddingModel":
        """Get the singleton instance of the embedding model.
        
        Returns:
            Embedding model instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the embedding model."""
        self._model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )
    
    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed a list of documents.
        
        Args:
            documents: List of documents to embed
            
        Returns:
            List of document embeddings
        """
        return self._model.embed_documents(documents)
    
    def embed_query(self, query: str) -> list[float]:
        """Embed a query.
        
        Args:
            query: Query to embed
            
        Returns:
            Query embedding
        """
        return self._model.embed_query(query)

def get_embeddings() -> OpenAIEmbeddingModel:
    """Get the embeddings model instance.
    
    Returns:
        Embeddings model instance
    """
    return OpenAIEmbeddingModel.get_instance() 