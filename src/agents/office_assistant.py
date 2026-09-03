"""
Main Office Assistant.

Coordinates all AI components.
"""

from src.agents.intent_classifier import IntentClassifier
from src.agents.router import Router
from src.models.routes import Route
from src.models.state import AgentState


class OfficeAssistant:

    def __init__(self):

        self.intent_classifier = IntentClassifier()
        self.router = Router()

    def process_query(self, user_query: str) -> AgentState:
        state = AgentState(user_query=user_query)
        state.intent = self.intent_classifier.classify(
            state.user_query
            )
        state.route = self.router.route(
            state.intent
            )
        if state.route == Route.RAG:
            state.response = "Routing request to RAG module..."
        elif state.route == Route.EMPLOYEE_DATA:
            state.response = "Routing request to Employee Data Tool..."
        elif state.route == Route.ACTION:
            state.response = "Routing request to Action Tool..."
        else:
            state.response = "Sorry, I couldn't understand your request."

        return state