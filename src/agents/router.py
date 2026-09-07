"""
Router module.

Maps intents to the correct subsystem.
"""

from src.models.intents import Intent
from src.models.routes import Route


class Router:
    """
    Decides which subsystem should handle a request.
    """

    def route(self, intent: Intent) -> Route:

        if intent == Intent.POLICY_QUERY:
            return Route.RAG

        elif intent == Intent.UNKNOWN:
            return Route.UNKNOWN

        else:
            return Route.MCP