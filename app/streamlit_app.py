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
# Helper Functions
# ---------------------------------------------------------

def format_tool_response(response):
    """
    Convert structured MCP responses into user-friendly
    Streamlit output.

    MCP tools continue returning dictionaries.
    This function only controls how those results are
    presented to the employee.
    """

    if not isinstance(response, dict):
        return response

    # -----------------------------------------------------
    # Leave Balance
    # -----------------------------------------------------

    if "leave_balance" in response:

        balance = response["leave_balance"]

        st.markdown("### 🏖️ Your Leave Balance")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Casual Leave",
                f"{balance['casual_leave']} days",
            )

        with col2:
            st.metric(
                "Earned Leave",
                f"{balance['earned_leave']} days",
            )

        with col3:
            st.metric(
                "Sick Leave",
                f"{balance['sick_leave']} days",
            )

        return None

    # -----------------------------------------------------
    # Assigned Assets
    # -----------------------------------------------------

    if "assets" in response:

        assets = response["assets"]

        st.markdown("### 💻 Assets Assigned to You")

        if not assets:
            st.info("No assets are currently assigned to you.")
            return None

        for asset in assets:

            with st.container(border=True):

                st.markdown(
                    f"#### {asset['asset_name']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Asset Type:** {asset['asset_type']}"
                    )
                    st.write(
                        f"**Asset ID:** {asset['asset_id']}"
                    )
                    st.write(
                        f"**Serial Number:** {asset['serial_number']}"
                    )

                with col2:
                    st.write(
                        f"**Status:** {asset['status']}"
                    )
                    st.write(
                        f"**Assigned Date:** {asset['assigned_date']}"
                    )

        return None

    # -----------------------------------------------------
    # Leave Requests
    # -----------------------------------------------------

    if "requests" in response:

        requests = response["requests"]

        st.markdown("### 📋 Your Leave Requests")

        if not requests:
            st.info("You don't have any leave requests.")
            return None

        for request in requests:

            with st.container(border=True):

                st.markdown(
                    f"#### {request['leave_type']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Request ID:** {request['request_id']}"
                    )
                    st.write(
                        f"**Start Date:** {request['start_date']}"
                    )
                    st.write(
                        f"**End Date:** {request['end_date']}"
                    )

                with col2:
                    st.write(
                        f"**Days:** {request['days']}"
                    )
                    st.write(
                        f"**Status:** {request['status']}"
                    )
                    st.write(
                        f"**Created:** {request['created_at']}"
                    )

        return None

    # -----------------------------------------------------
    # Generic MCP Response
    # -----------------------------------------------------

    if response.get("success") is False:

        return response.get(
            "message",
            "The request could not be completed.",
        )

    if response.get("success") is True:

        return response.get(
            "message",
            "Request completed successfully.",
        )

    return response


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
        "⚠️ Confirmation required before this action can be executed."
    )

    if action.get("action_type") == "submit_leave":

        st.subheader("🏖️ Leave Request")

        st.write(
            f"**Employee:** {action['employee_id']}"
        )

        st.write(
            f"**Leave Type:** {action['leave_type'].title()}"
        )

        st.write(
            f"**Start Date:** {action['start_date']}"
        )

        st.write(
            f"**End Date:** {action['end_date']}"
        )

        st.write(
            f"**Days:** {action['days']}"
        )

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # Confirm
        # -------------------------------------------------

        with col1:

            if st.button(
                "✅ Confirm",
                use_container_width=True,
            ):

                confirmation_result = (
                    validate_action_confirmation(True)
                )

                if confirmation_result["valid"]:

                    result = (
                        st.session_state.assistant
                        .tool_dispatcher
                        .execute(
                            intent=Intent.SUBMIT_LEAVE,
                            employee_id=action["employee_id"],
                            leave_type=action["leave_type"],
                            start_date=action["start_date"],
                            end_date=action["end_date"],
                        )
                    )

                    if (
                        isinstance(result, dict)
                        and result.get("success")
                    ):

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

        # -------------------------------------------------
        # Cancel
        # -------------------------------------------------

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

    # -----------------------------------------------------
    # Store User Message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------------------------------
    # Activity
    # -----------------------------------------------------

    st.session_state.activity.append(
        "Request received."
    )

    st.session_state.activity.append(
        f"Employee session: "
        f"{st.session_state.current_employee_id}"
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

        # -------------------------------------------------
        # Pending Action
        # -------------------------------------------------

        if state.pending_action:

            st.session_state.pending_action = (
                state.pending_action
            )

            st.session_state.activity.append(
                "Validation passed."
            )

            st.session_state.activity.append(
                "Confirmation required before action."
            )

        # -------------------------------------------------
        # Intent
        # -------------------------------------------------

        if state.intent:

            st.session_state.activity.append(
                f"Intent identified: "
                f"{state.intent.value}"
            )

        # -------------------------------------------------
        # Route
        # -------------------------------------------------

        if state.route:

            st.session_state.activity.append(
                f"Route selected: "
                f"{state.route.value}"
            )

        # -------------------------------------------------
        # RAG Activity
        # -------------------------------------------------

        if state.route == Route.RAG:

            st.session_state.activity.append(
                "Retrieved relevant company policy."
            )

            if state.citations:

                st.session_state.activity.append(
                    f"Retrieved "
                    f"{len(state.citations)} citation(s)."
                )

        # -------------------------------------------------
        # MCP Activity
        # -------------------------------------------------

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
                "I couldn't find a response "
                "for that request."
            )

        with st.chat_message("assistant"):

            # -------------------------------------------------
            # Structured MCP Response
            # -------------------------------------------------

            formatted_response = (
                format_tool_response(response)
            )

            # -------------------------------------------------
            # Normal Text Response
            # -------------------------------------------------

            if formatted_response is not None:

                st.markdown(formatted_response)

            # -------------------------------------------------
            # RAG Sources
            # -------------------------------------------------

            if state.citations:

                with st.expander("📚 Sources"):

                    for citation in state.citations:

                        st.write(citation)

        # -----------------------------------------------------
        # Store Assistant Message
        #
        # For structured MCP responses we store a clean
        # text summary rather than the raw dictionary.
        # -----------------------------------------------------

        if isinstance(response, dict):

            if "leave_balance" in response:

                balance = response["leave_balance"]

                stored_response = (
                    f"Your leave balance: "
                    f"Casual Leave: {balance['casual_leave']} days, "
                    f"Earned Leave: {balance['earned_leave']} days, "
                    f"Sick Leave: {balance['sick_leave']} days."
                )

            elif "assets" in response:

                assets = response["assets"]

                if assets:

                    asset_names = ", ".join(
                        asset["asset_name"]
                        for asset in assets
                    )

                    stored_response = (
                        f"Your assigned assets: "
                        f"{asset_names}."
                    )

                else:

                    stored_response = (
                        "You currently have "
                        "no assigned assets."
                    )

            elif "requests" in response:

                requests = response["requests"]

                stored_response = (
                    f"You have {len(requests)} "
                    f"leave request(s)."
                )

            elif "message" in response:

                stored_response = response["message"]

            else:

                stored_response = str(response)

        else:

            stored_response = str(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": stored_response,
            }
        )

    # -----------------------------------------------------
    # Error Handling
    # -----------------------------------------------------

    except Exception as exc:

        error_message = (
            "I’m sorry, but I couldn't process "
            "that request right now."
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