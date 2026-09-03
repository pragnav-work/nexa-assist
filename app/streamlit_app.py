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


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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