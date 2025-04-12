"""Graph definition for the RAG application."""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import Graph

from ..config.settings import settings
from .tools import retrieve_documents

def create_graph() -> Graph:
    """Create the RAG graph using a prebuilt React agent.
    
    The graph uses a React agent with a retrieval tool to search for relevant documents
    and generate responses based on the retrieved information.
    
    Returns:
        Graph: The configured RAG graph
    """
    # Initialize the model with API key from settings
    model = ChatOpenAI(
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        api_key=settings.OPENAI_API_KEY
    )
    
    # Create the React agent graph with our retrieval tool
    graph = create_react_agent(model, tools=[retrieve_documents])

    return graph

