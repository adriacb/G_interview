"""Base classes and interfaces for the RAG application."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, TypedDict

class Document(TypedDict):
    """Represents a document in the system."""
    id: str
    content: str
    metadata: Dict[str, Any]

class QueryResult(TypedDict):
    """Represents a query result from the vector store."""
    document: Document
    score: float

class VectorStore(Protocol):
    """Interface for vector store implementations."""
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        ...
    
    def search(self, query: str, k: int = 5) -> List[QueryResult]:
        """Search for similar documents."""
        ...
    
    def delete_document(self, document_id: str) -> None:
        """Delete a document from the vector store."""
        ...

class DocumentProcessor(ABC):
    """Abstract base class for document processing."""
    
    @abstractmethod
    def process_document(self, document: Document) -> Document:
        """Process a single document."""
        pass
    
    @abstractmethod
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process multiple documents."""
        pass

class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for a text."""
        pass
    
    @abstractmethod
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """Generate embeddings for multiple documents."""
        pass

class Retriever(ABC):
    """Abstract base class for document retrieval."""
    
    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve relevant documents for a query."""
        pass

class ResponseGenerator(ABC):
    """Abstract base class for response generation."""
    
    @abstractmethod
    def generate_response(
        self,
        query: str,
        context: List[Document],
        **kwargs: Any
    ) -> str:
        """Generate a response based on query and context."""
        pass

class Node(ABC):
    """Abstract base class for graph nodes."""
    
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the node's logic and update state."""
        pass

class Tool(ABC):
    """Abstract base class for tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the description of the tool."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with given parameters."""
        pass

class StateManager(ABC):
    """Abstract base class for state management."""
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Get the current state."""
        pass
    
    @abstractmethod
    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update the state with new values."""
        pass
    
    @abstractmethod
    def clear_state(self) -> None:
        """Clear the current state."""
        pass 