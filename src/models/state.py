"""
Shared state used by the Office Assistant.
"""

from dataclasses import dataclass, field

from src.models.intents import Intent
from src.models.routes import Route


@dataclass
class AgentState:

    user_query: str

    intent: Intent | None = None

    route: Route | None = None

    response: str = ""

    citations: list[str] = field(default_factory=list)