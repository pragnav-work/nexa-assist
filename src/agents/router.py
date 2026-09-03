"""
Router module.

Maps intents to the correct subsystem.
"""

from src.models.intents import Intent
from src.models.routes import Route


class Router:

    def route(self, intent: Intent) -> Route:
        """
        Decide which subsystem should handle the request.
        """

        routing_table = {
            Intent.POLICY_QUERY: Route.RAG,
            Intent.EMPLOYEE_DATA: Route.EMPLOYEE_DATA,
            Intent.ACTION_REQUEST: Route.ACTION,
            Intent.UNKNOWN: Route.UNKNOWN,
        }

        return routing_table.get(intent, Route.UNKNOWN)