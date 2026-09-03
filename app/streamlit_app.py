import streamlit as st


st.set_page_config(
    page_title="NexaAssist",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 NexaAssist")
st.caption("AI Enterprise Employee Assistant")


st.sidebar.header("Employee Session")

employee = st.sidebar.selectbox(
    "Select employee",
    [
        "NC1001 - Pragna",
        "NC1002 - Pavan",
        "NC1003 - Sankalp",
        "NC1004 - Chinmay"
    ],
)

current_employee_id = employee.split(" - ")[0]

st.sidebar.divider()

st.sidebar.subheader("Current Session")
st.sidebar.write(f"Employee ID: **{current_employee_id}**")

st.sidebar.divider()

st.sidebar.subheader("Capabilities")
st.sidebar.write("• Company policy questions")
st.sidebar.write("• Leave information")
st.sidebar.write("• Expense information")
st.sidebar.write("• IT requests")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.pending_action:
    action = st.session_state.pending_action

    st.info("⚠️ Confirmation required before this action can be executed.")

    st.subheader("Leave Request")

    st.write(f"**Employee:** {action['employee_id']}")
    st.write(f"**Leave Type:** {action['leave_type']}")
    st.write(f"**Start Date:** {action['start_date']}")
    st.write(f"**End Date:** {action['end_date']}")
    st.write(f"**Days:** {action['days']}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Confirm", use_container_width=True):
            st.success("Leave request confirmed. MCP action will be connected next.")
            st.session_state.pending_action = None

    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.warning("Leave request cancelled.")
            st.session_state.pending_action = None

if st.button("Test Leave Confirmation"):
    st.session_state.pending_action = {
        "employee_id": current_employee_id,
        "leave_type": "earned_leave",
        "start_date": "2026-09-10",
        "end_date": "2026-09-12",
        "days": 3,
    }
    st.rerun()

user_input = st.chat_input(
    "Ask NexaAssist something..."
)


if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = (
        f"Hello! I received your request as employee "
        f"**{current_employee_id}**.\n\n"
        "The NexaAssist agent will be connected here next."
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response)