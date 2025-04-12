"""Tools for the RAG application."""
from typing import List, Dict, Any
from langchain_core.tools import tool
from ..utils.logging import get_logger
from .vector_store import get_vector_store

logger = get_logger(__name__)

@tool
def retrieve_documents(query: str) -> List[Dict[str, Any]]:
    """Use it always to answer questions about VOLKSWAGEN.

    It returns the most similar documents along with their metadata and similarity scores.
    
    Args:
        query: The search query to find relevant documents
        
    Returns:
        List of relevant documents with their content, metadata, and similarity scores
    """
    try:
        # Get vector store instance
        vector_store = get_vector_store()
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        return []
        
    # Search for documents
    results = vector_store.search(query, k=5)
    logger.info(f"Results: {results}")
    # Format results for the agent
    return [
        {
            "content": result['document']["content"],
            "metadata": result['document']["metadata"],
            "score": result["score"]
        }
        for result in results
    ] 