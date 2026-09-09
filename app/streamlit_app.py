import streamlit as st

from src.models.intents import Intent

from src.validation.validator import validate_action_confirmation

from src.agents.office_assistant import OfficeAssistant
from src.models.routes import Route


st.set_page_config(
    page_title="NexaAssist",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# App Configuration
# ---------------------------------------------------------

st.title("🤖 NexaAssist")
st.caption("AI Enterprise Employee Assistant")


# ---------------------------------------------------------
# Employee Session
# ---------------------------------------------------------

st.sidebar.header("Employee Session")

employee = st.sidebar.selectbox(
    "Select employee",
    [
        "NC1001 - Pragna",
        "NC1002 - Pavan",
        "NC1003 - Sankalp",
        "NC1004 - Chinmay",
    ],
)

current_employee_id = employee.split(" - ")[0]

# Application session is the source of truth for identity.
st.session_state.current_employee_id = current_employee_id

st.sidebar.divider()

st.sidebar.subheader("Current Session")
st.sidebar.write(
    f"Employee ID: **{st.session_state.current_employee_id}**"
)

st.sidebar.divider()

st.sidebar.subheader("Capabilities")
st.sidebar.write("• Company policy questions")
st.sidebar.write("• Leave information")
st.sidebar.write("• Expense information")
st.sidebar.write("• IT requests")


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "activity" not in st.session_state:
    st.session_state.activity = []

if "assistant" not in st.session_state:
    st.session_state.assistant = OfficeAssistant()


# ---------------------------------------------------------
# Activity
# ---------------------------------------------------------

if st.session_state.activity:
    with st.expander("Activity", expanded=False):
        for item in st.session_state.activity:
            st.write(f"• {item}")


# ---------------------------------------------------------
# Chat History
# ---------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# Pending Action Confirmation
# ---------------------------------------------------------

if st.session_state.pending_action:

    action = st.session_state.pending_action

    st.warning(
        "Confirmation required before this action can be executed."
    )

    if action.get("action_type") == "submit_leave":

        st.subheader("Leave Request")

        st.write(f"**Employee:** {action['employee_id']}")
        st.write(f"**Leave Type:** {action['leave_type'].title()}")
        st.write(f"**Start Date:** {action['start_date']}")
        st.write(f"**End Date:** {action['end_date']}")
        st.write(f"**Days:** {action['days']}")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Confirm",
                use_container_width=True,
            ):

                confirmation_result = validate_action_confirmation(
                    True
                )

                if confirmation_result["valid"]:

                    result = st.session_state.assistant.tool_dispatcher.execute(
                        intent=Intent.SUBMIT_LEAVE,
                        employee_id=action["employee_id"],
                        leave_type=action["leave_type"],
                        start_date=action["start_date"],
                        end_date=action["end_date"],
                    )

                    if isinstance(result, dict) and result.get("success"):

                        st.session_state.activity.append(
                            "Leave request confirmed."
                        )

                        st.session_state.activity.append(
                            "Leave request submitted through MCP."
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": result["message"],
                            }
                        )

                        st.session_state.pending_action = None

                        st.rerun()

                    else:

                        message = (
                            result.get("message")
                            if isinstance(result, dict)
                            else str(result)
                        )

                        st.error(message)

        with col2:

            if st.button(
                "❌ Cancel",
                use_container_width=True,
            ):

                st.session_state.activity.append(
                    "Leave request cancelled."
                )

                st.session_state.pending_action = None

                st.rerun()

# ---------------------------------------------------------
# Chat Input
# ---------------------------------------------------------

user_input = st.chat_input(
    "Ask NexaAssist something..."
)


if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Activity
    st.session_state.activity.append(
        "Request received."
    )

    st.session_state.activity.append(
        f"Employee session: {st.session_state.current_employee_id}"
    )

    # -----------------------------------------------------
    # Agent Processing
    # -----------------------------------------------------

    try:

        assistant = st.session_state.assistant

        state = assistant.process_query(
            user_query=user_input,
            employee_id=st.session_state.current_employee_id,
            conversation_history=st.session_state.messages[:-1],
        )

        if state.pending_action:
            st.session_state.pending_action = state.pending_action

        # Record intent
        if state.intent:
            st.session_state.activity.append(
                f"Intent identified: {state.intent.value}"
            )

        # Record route
        if state.route:
            st.session_state.activity.append(
                f"Route selected: {state.route.value}"
            )

        # RAG activity
        if state.route == Route.RAG:

            st.session_state.activity.append(
                "Retrieved relevant company policy."
            )

            if state.citations:
                st.session_state.activity.append(
                    f"Retrieved {len(state.citations)} citation(s)."
                )

        # MCP activity
        elif state.route == Route.MCP:

            st.session_state.activity.append(
                "Retrieved employee-specific information."
            )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        response = state.response

        if not response:
            response = (
                "I couldn't find a response for that request."
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(response)

            # Show citations when available
            if state.citations:

                with st.expander("Sources"):

                    for citation in state.citations:
                        st.write(citation)

    except Exception as exc:

        error_message = (
            "I’m sorry, but I couldn't process that request right now."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.activity.append(
            "Request processing failed."
        )

        st.session_state.activity.append(
            f"Error: {type(exc).__name__}"
        )
