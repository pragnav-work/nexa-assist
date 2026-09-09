"""
Main Office Assistant.

Coordinates all AI components while keeping
employee identity controlled by the application session.
"""

import re
from datetime import date

from src.agents.intent_classifier import IntentClassifier
from src.agents.router import Router
from src.models.routes import Route
from src.models.state import AgentState
from src.models.intents import Intent

from src.tools.tool_dispatcher import ToolDispatcher
from src.tools.leave_tools import get_leave_balance

from src.rag.pipeline import RAGPipeline

from src.validation.validator import (
    validate_employee_context,
    validate_leave_request,
)


class OfficeAssistant:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.router = Router()

        self.rag_engine = RAGPipeline()

        self.tool_dispatcher = ToolDispatcher()
    # -----------------------------------------------------
    # Employee ID extraction
    # -----------------------------------------------------

    def _extract_requested_employee_id(
        self,
        user_query: str,
    ) -> str | None:

        if not user_query:
            return None

        match = re.search(
            r"\bNC\d{4}\b",
            user_query.upper(),
        )

        if match:
            return match.group(0)

        return None

    # -----------------------------------------------------
    # Leave request extraction
    # -----------------------------------------------------

    def _extract_leave_request(
        self,
        user_query: str,
        conversation_history: list[dict] | None = None,
    ) -> dict | None:
        """
    Deterministically extracts leave information.

    Supports:
    - Explicit leave requests with YYYY-MM-DD dates
    - Follow-ups such as:
      "Can I use 3 of them next week?"
        """

        if not user_query:
            return None

        text = user_query.lower()

    # -------------------------------------------------
    # Leave type
    # -------------------------------------------------

        leave_type = None

        leave_type_patterns = {
            "casual leave": r"\bcasual\s+leave\b",
            "earned leave": r"\bearned\s+leave\b",
            "sick leave": r"\bsick\s+leave\b",
        }

        for name, pattern in leave_type_patterns.items():
            if re.search(pattern, text):
                leave_type = name
                break

    # If follow-up does not mention leave type,
    # recover it from recent conversation.
        if not leave_type and conversation_history:

            for message in reversed(conversation_history):

                content = message.get("content", "").lower()

                for name, pattern in leave_type_patterns.items():

                    if re.search(pattern, content):
                        leave_type = name
                        break

                if leave_type:
                    break

    # -------------------------------------------------
    # Explicit dates
    # -------------------------------------------------

        dates = re.findall(
            r"\b\d{4}-\d{2}-\d{2}\b",
            user_query,
        )

        start_date = None
        end_date = None

        if len(dates) >= 2:

            try:
                start_date = date.fromisoformat(dates[0])
                end_date = date.fromisoformat(dates[1])
            except ValueError:
                return None

    # -------------------------------------------------
    # Requested number of days
    # -------------------------------------------------

        requested_days = None

        days_match = re.search(
            r"\b(\d+)\s+(?:days?|of\s+(?:them|those|these))\b",
            text,
        )

        if days_match:
            requested_days = int(days_match.group(1))

    # -------------------------------------------------
    # "next week"
    # -------------------------------------------------

        if "next week" in text and requested_days:

            today = date.today()

            days_until_monday = (7 - today.weekday()) % 7

            if days_until_monday == 0:
                days_until_monday = 7

            start_date = today.fromordinal(
                today.toordinal() + days_until_monday
            )

            end_date = start_date.fromordinal(
                start_date.toordinal() + requested_days - 1
            )

    # -------------------------------------------------
    # Calculate days for explicit date range
    # -------------------------------------------------

        if (
            requested_days is None
            and start_date
            and end_date
        ):
            requested_days = (
                end_date - start_date
            ).days + 1

    # -------------------------------------------------
    # Required fields
    # -------------------------------------------------

        if (
            not leave_type
            or not start_date
            or not end_date
            or not requested_days
        ):
            return None

        return {
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "requested_days": requested_days,
        }

    # -----------------------------------------------------
    # Main processing
    # -----------------------------------------------------

    def process_query(
        self,
        user_query: str,
        employee_id: str,
        conversation_history: list[dict] | None = None,
    ) -> AgentState:

        state = AgentState(
            user_query=user_query,
            employee_id=employee_id,
        )

        # -------------------------------------------------
        # Step 1: Employee isolation
        # -------------------------------------------------

        requested_employee_id = (
            self._extract_requested_employee_id(user_query)
        )

        if requested_employee_id:

            validation_result = validate_employee_context(
                session_employee_id=employee_id,
                requested_employee_id=requested_employee_id,
            )

            if not validation_result["valid"]:

                state.response = (
                    "I can only provide employee-specific information "
                    "for the employee currently selected in this session."
                )

                return state

        # -------------------------------------------------
        # Step 2: Classify intent
        # -------------------------------------------------

        state.intent = self.intent_classifier.classify(
            state.user_query,
            conversation_history=conversation_history,
        )

        # -------------------------------------------------
        # Step 3: Route request
        # -------------------------------------------------

        state.route = self.router.route(
            state.intent
        )

        # -------------------------------------------------
        # Step 4: Leave application
        # -------------------------------------------------

        if state.intent == Intent.SUBMIT_LEAVE:

            leave_data = self._extract_leave_request(
                user_query,
                conversation_history=conversation_history,
            )

            if not leave_data:

                state.response = (
                    "I can help you apply for leave. "
                    "Please provide the leave type and dates "
                    "in YYYY-MM-DD format. For example: "
                    "'I want earned leave from 2026-09-15 "
                    "to 2026-09-17.'"
                )

                return state

            # Retrieve current balance
            balance_result = get_leave_balance(
                employee_id
            )

            if not balance_result.get("success"):

                state.response = (
                    "I couldn't retrieve your leave balance "
                    "right now."
                )

                return state

            balance = balance_result["leave_balance"]

            column_map = {
                "casual leave": "casual_leave",
                "earned leave": "earned_leave",
                "sick leave": "sick_leave",
            }

            balance_column = column_map[
                leave_data["leave_type"]
            ]

            available_balance = int(
                balance[balance_column]
            )

            # Validate everything deterministically
            validation_result = validate_leave_request(
                session_employee_id=employee_id,
                requested_employee_id=employee_id,
                leave_type=leave_data["leave_type"],
                start_date=leave_data["start_date"],
                end_date=leave_data["end_date"],
                requested_days=leave_data["requested_days"],
                available_balance=available_balance,
            )

            if not validation_result["valid"]:

                state.response = (
                    "I can't submit this leave request because:\n\n"
                    + "\n".join(
                        f"- {error}"
                        for error in validation_result["errors"]
                    )
                )

                return state

            # Do NOT call apply_leave() here.
            # Store the action for explicit confirmation.

            state.pending_action = {
                "action_type": "submit_leave",
                "employee_id": employee_id,
                "leave_type": leave_data["leave_type"],
                "start_date": leave_data["start_date"].isoformat(),
                "end_date": leave_data["end_date"].isoformat(),
                "days": leave_data["requested_days"],
            }

            state.response = (
                "Your leave request is ready for confirmation."
            )

            return state

        # -------------------------------------------------
        # Step 5: Execute the selected route
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Step 6: MCP read-only tools
        # -------------------------------------------------

        elif state.route == Route.MCP:

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
