"""Document processor module for the RAG application."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument
from langchain_core.documents import Document as LangChainDocument
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
import os
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor(ABC):
    """Abstract base class for document processing."""
    
    @abstractmethod
    def process_document(self, document_path: str) -> Dict[str, Any]:
        """Process a document and return its content and metadata.
        
        Args:
            document_path: Path to the document to process
            
        Returns:
            Dictionary containing the document content and metadata
        """
        pass
    
    @abstractmethod
    def extract_text(self, document_path: str) -> str:
        """Extract text from a document.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Extracted text
        """
        pass
    
    @abstractmethod
    def get_metadata(self, document_path: str) -> Dict[str, Any]:
        """Get metadata from a document.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Document metadata
        """
        pass


class DoclingProcessor(DocumentProcessor):
    """Document processor implementation using Docling."""
    
    def __init__(self, converter: Optional[DocumentConverter] = None):
        """Initialize the DoclingProcessor.

        Args:
            converter (Optional[DocumentConverter], optional): Document converter instance. 
                If None, creates a new one with default settings. Defaults to None.
        """
        if converter is None:
            converter = DocumentConverter()
        self.converter = converter
        
        # Initialize markdown splitter for headers
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                # ("###", "Header 3"),
                # ("####", "Header 4"),
            ]
        )
    
    def get_metadata(self, document_path: str) -> Dict[str, Any]:
        """Get metadata from a document.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Dictionary containing document metadata
        """
        return self._extract_metadata(document_path)
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a document and return its content and metadata.
        
        Args:
            file_path: Path to the document to process
            
        Returns:
            Dictionary containing:
            - content: The processed document content
            - metadata: Document metadata
            - chunks: List of document chunks with header metadata
        """
        try:
            # Get document metadata
            metadata = self._extract_metadata(file_path)
            
            # Extract text from document
            content = self.extract_text(file_path)
            if not content:
                logger.error(f"Failed to extract text from {file_path}")
                return None
            
            # Split by headers to maintain document structure
            chunks = []
            header_chunks = self.markdown_splitter.split_text(content)
            
            for chunk in header_chunks:
                chunks.append({
                    "content": chunk.page_content,
                    "metadata": {**metadata, **chunk.metadata}
                })
            
            return {
                "content": content,
                "metadata": metadata,
                "chunks": chunks
            }
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            return None
    
    def extract_text(self, document_path: str) -> str:
        """Extract text from a document using Docling.
        
        Args:
            document_path: Path to the document
            
        Returns:
            Extracted text in markdown format
        """
        try:
            result = self.converter.convert(document_path)
            return result.document.export_to_markdown()
        except Exception as e:
            logger.error(f"Error extracting text from {document_path}: {str(e)}")
            return ""
    
    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from a document.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dict containing the metadata
        """
        return {
            "filename": os.path.basename(file_path),
            "file_size": os.path.getsize(file_path),
            "file_type": os.path.splitext(file_path)[1]
        } 