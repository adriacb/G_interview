"""Agent module for the RAG application."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Agent(ABC):
    """Abstract base class for the RAG agent."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the agent."""
        pass
    
    @abstractmethod
    def process_query(self, query: str) -> str:
        """Process a query and return an answer.
        
        Args:
            query: The query to process
            
        Returns:
            The answer to the query
        """
        pass
    
    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get the tools available to the agent.
        
        Returns:
            List of tool definitions
        """
        pass
    
    @abstractmethod
    def add_tool(self, tool: Dict[str, Any]) -> None:
        """Add a tool to the agent.
        
        Args:
            tool: Tool definition to add
        """
        pass 