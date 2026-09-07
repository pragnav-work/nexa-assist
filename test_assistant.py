from src.agents.office_assistant import OfficeAssistant

assistant = OfficeAssistant()

state = assistant.process_query(
    user_query="How many WFH days can I take?",
    employee_id="EMP001"
)

print(state.response)
print(state.citations)