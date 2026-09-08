"""
Main Office Assistant.

Coordinates all AI components.
"""

from src.agents.intent_classifier import IntentClassifier
from src.agents.router import Router

from src.models.routes import Route
from src.models.state import AgentState

from src.tools.tool_dispatcher import ToolDispatcher
from src.rag.pipeline import RAGPipeline


class OfficeAssistant:

    def __init__(self):

        self.intent_classifier = IntentClassifier()
        self.router = Router()

        # RAG Engine
        self.rag_engine = RAGPipeline()

        # MCP Tool Dispatcher
        self.tool_dispatcher = ToolDispatcher()

    def process_query(
        self,
        user_query: str,
        employee_id: str,
    ) -> AgentState:

        state = AgentState(
            user_query=user_query,
            employee_id=employee_id,
        )

        # Step 1: Classify the request
        state.intent = self.intent_classifier.classify(
            state.user_query
        )

        # Step 2: Decide where to route it
        state.route = self.router.route(
            state.intent
        )

        # Step 3: Execute the selected route
        if state.route == Route.GREETING:

            state.response = (
        "Hello! I'm NexaAssist. "
        "I can help you with company policies, leave management, "
        "expenses, employee information, office details, and IT assets. "
        "How can I assist you today?"
          )

        elif state.route == Route.RAG:

            result = self.rag_engine.answer_query(
        state.user_query
        )

            state.response = result["answer"]
            state.citations = result["citations"]

        elif state.route == Route.MCP:

        # Store selected MCP tool
            state.tool_name = state.intent.value

            state.response = self.tool_dispatcher.execute(
            intent=state.intent,
            employee_id=state.employee_id,
            query=state.user_query,
            )

        else:

            state.response = (
        "Sorry, I couldn't understand your request."
            )

        return state