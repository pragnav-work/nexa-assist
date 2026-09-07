"""
Defines all possible routes inside the Office Assistant.
"""

from enum import Enum


class Route(str, Enum):
    RAG = "rag"
    MCP = "mcp"
    UNKNOWN = "unknown"