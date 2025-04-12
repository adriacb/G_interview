"""State management for the RAG application."""
from typing import Annotated, List
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    """State for the RAG application.
    
    This state is used to pass information between nodes in the graph.
    It includes:
    - messages: List of messages in the conversation
    - user_id: Unique identifier for the user
    - context: Additional context for the current state
    """
    messages: Annotated[List[BaseMessage], add_messages]
    user_id: str
    context: dict 