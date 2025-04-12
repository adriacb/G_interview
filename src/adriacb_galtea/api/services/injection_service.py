"""Service for document injection into the vector store."""
from typing import List, Dict, Any
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException

from ...core.document_processor import DoclingProcessor
from ...core.vector_store import ChromaVectorStore, get_vector_store
from ...utils.logging import get_logger

logger = get_logger(__name__)

class InjectionService:
    """Service for injecting documents into the vector store."""
    
    def __init__(self):
        """Initialize the injection service."""
        self.processor = DoclingProcessor()
        self.vector_store = get_vector_store()
    
    def _process_chunks(self, chunks: List[Dict[str, Any]], file_path: str) -> List[Dict[str, Any]]:
        """Process chunks before storage, including header metadata.
        
        Args:
            chunks: List of chunks to process
            file_path: Path to the source document
            
        Returns:
            List of processed chunks ready for storage
        """
        processed_chunks = []
        
        for i, chunk in enumerate(chunks):
            metadata = chunk.get("metadata", {}).copy()
            
            # Extract headers if present
            headers = {k: v for k, v in metadata.items() if k.lower().startswith("header")}
            
            # Flatten headers into a single field for better searchability
            metadata["headers"] = " > ".join([v for k, v in sorted(headers.items()) if v])
            
            # Add source file to metadata
            metadata["source_file"] = file_path
            
            processed_chunk = {
                "id": f"{str(hash(file_path))}_{i}",
                "content": chunk["content"],
                "metadata": metadata
            }
            
            processed_chunks.append(processed_chunk)
            
        return processed_chunks
    
    def inject_document(self, file_path: str, max_chunks: int = 500) -> Dict[str, Any]:
        """Inject a document into the vector store.
        
        Args:
            file_path: Path to the document to inject
            max_chunks: Maximum number of chunks to store
            
        Returns:
            Dictionary containing:
            - success: Whether the injection was successful
            - message: Status message
            - chunks_processed: Number of chunks processed
        """
        try:
            # Convert to absolute path if needed
            file_path = str(Path(file_path).resolve())
            
            if not Path(file_path).exists():
                return {
                    "success": False,
                    "message": f"File not found: {file_path}",
                    "chunks_processed": 0
                }
            
            # Process document
            logger.info("processing_document", file_path=file_path)
            result = self.processor.process_document(file_path)
            
            if not result:
                return {
                    "success": False,
                    "message": f"Failed to process document: {file_path}",
                    "chunks_processed": 0
                }
            
            # Process chunks
            chunks = result.get("chunks", [])
            if len(chunks) > max_chunks:
                logger.warning("chunk_limit_reached", max_chunks=max_chunks, total_chunks=len(chunks))
                chunks = chunks[:max_chunks]
            
            processed_chunks = self._process_chunks(chunks, file_path)
            
            # Store chunks
            logger.info("storing_chunks", count=len(processed_chunks))
            self.vector_store.add_documents(processed_chunks)
            
            return {
                "success": True,
                "message": "Document successfully injected",
                "chunks_processed": len(processed_chunks)
            }
            
        except Exception as e:
            logger.error("error_injecting_document", error=str(e), exc_info=True)
            return {
                "success": False,
                "message": f"Error injecting document: {str(e)}",
                "chunks_processed": 0
            }
    
    async def inject_documents(self, files: List[UploadFile]) -> List[dict]:
        """Inject multiple documents into the vector store.
        
        Args:
            files: List of files to inject
            
        Returns:
            List of injection results
        """
        results = []
        for file in files:
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
                    result = self.inject_document(temp_path)
                    results.append(result)
                finally:
                    # Clean up temporary file
                    os.unlink(temp_path)
                    
            except Exception as e:
                logger.error("error_processing_file", filename=file.filename, error=str(e), exc_info=True)
                results.append({
                    "success": False,
                    "message": f"Failed to process {file.filename}: {str(e)}",
                    "chunks_processed": 0
                })
                
        return results
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store.
        
        Args:
            doc_id: ID of the document to delete
            
        Returns:
            Whether the deletion was successful
        """
        try:
            self.vector_store.delete_document(doc_id)
            return True
        except Exception as e:
            logger.error("error_deleting_document", doc_id=doc_id, error=str(e), exc_info=True)
            return False 