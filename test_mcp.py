from src.agents.office_assistant import OfficeAssistant

assistant = OfficeAssistant()

state = assistant.process_query(
    user_query="How many leave days do I have?",
    employee_id="NC1001"
)

print("Intent:", state.intent)
print("Route:", state.route)
print("Tool:", state.tool_name)
print("Response:", state.response)