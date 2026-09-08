from src.agents.office_assistant import OfficeAssistant

assistant = OfficeAssistant()

state = assistant.process_query(
    user_query="Show my leave balance",
    employee_id="NC1001"
)

print("Intent:", state.intent)
print("Route:", state.route)
print("Response:", state.response)