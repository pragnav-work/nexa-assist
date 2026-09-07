"""
Shared state used by the Office Assistant.
"""

from dataclasses import dataclass, field

from src.models.intents import Intent
from src.models.routes import Route


@dataclass
class AgentState:
    """
    Shared state passed between all agent components.
    """

    # Original user request
    user_query: str

    # Employee making the request
    employee_id: str | None = None

    # Intent detected by Gemini
    intent: Intent | None = None

    # Which subsystem will handle it
    route: Route | None = None

    # Name of the MCP tool executed
    tool_name: str | None = None

    # Final response returned to the user
    response: str | None = None

    # RAG citations
    citations: list[str] = field(default_factory=list)