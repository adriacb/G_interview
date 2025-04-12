"""Vector store module for the RAG application."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Protocol, runtime_checkable, ClassVar, Callable
import os
from pathlib import Path
import structlog

from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document as LangChainDocument
from langchain_chroma import Chroma
from chromadb.config import Settings
import chromadb

from .base import Document, QueryResult, VectorStore
from .embeddings import get_embeddings
from .config.settings import settings

# Get the vector store path from settings
VECTOR_STORE_PATH = settings.VECTOR_STORE_PATH

logger = structlog.get_logger(__name__)

class VectorStore(ABC):
    """Abstract base class for vector storage."""
    
    @abstractmethod
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Save the vector store to disk.
        
        Args:
            path: Path to save the vector store
        """
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """Load the vector store from disk.
        
        Args:
            path: Path to load the vector store from
        """
        pass


@runtime_checkable
class ChromaVectorStore(Protocol):
    """Vector store implementation using ChromaDB."""
    
    _instance: ClassVar[Optional["ChromaVectorStore"]] = None
    
    @classmethod
    def get_instance(cls) -> "ChromaVectorStore":
        """Get the singleton instance of the vector store.
        
        Returns:
            Vector store instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self, collection_name: str = "documents"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection to use
        """
        # Get the project root directory (three levels up from src)
        project_root = Path(__file__).parent.parent.parent.parent
        chroma_path = project_root / VECTOR_STORE_PATH
        
        # Log paths for debugging
        logger.info(
            "vector_store_paths",
            project_root=str(project_root.absolute()),
            vector_store_path=VECTOR_STORE_PATH,
            full_path=str(chroma_path.absolute()),
            exists=chroma_path.exists()
        )
        
        # Create the directory if it doesn't exist
        if not chroma_path.exists():
            logger.info("creating_vector_store_directory", path=str(chroma_path.absolute()))
            chroma_path.mkdir(parents=True, exist_ok=True)
        else:
            logger.info("vector_store_directory_exists", path=str(chroma_path.absolute()))
        
        # Log the vector store location
        logger.info("initializing_chromadb", path=str(chroma_path.absolute()))
        
        self._client = chromadb.PersistentClient(path=str(chroma_path))
        self._collection_name = collection_name
        self._embeddings = get_embeddings()
        
        # Create or get collection
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize LangChain Chroma
        self._store = Chroma(
            client=self._client,
            collection_name=collection_name,
            embedding_function=self._embeddings
        )
        
        # Log successful initialization
        logger.info(
            "chromadb_initialized",
            collection_name=collection_name,
            path=str(chroma_path.absolute())
        )
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        # Convert documents to LangChain format
        texts = []
        metadatas = []
        ids = []
        
        for doc in documents:
            texts.append(doc["content"])
            metadatas.append(doc["metadata"])
            ids.append(doc["id"])
        
        # Add documents to vector store
        self._store.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, k: int = 5) -> List[QueryResult]:
        """Search for documents in the vector store.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of search results
        """
        # Search using LangChain Chroma
        results = self._store.similarity_search_with_score(query, k=k)
        
        # Convert to SearchResult format
        search_results = []
        for doc, score in results:
            search_results.append(QueryResult(
                document={
                    "content": doc.page_content,
                    "metadata": doc.metadata
                },
                score=score
            ))
        
        return search_results
    
    def delete_document(self, document_id: str) -> None:
        """Delete a document from the vector store.
        
        Args:
            document_id: ID of the document to delete.
        """
        # Delete from ChromaDB
        self._store.delete(ids=[document_id])

def get_vector_store() -> ChromaVectorStore:
    """Get the vector store instance.
    
    Returns:
        Vector store instance
    """
    return ChromaVectorStore.get_instance() 