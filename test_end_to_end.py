from src.agents.office_assistant import OfficeAssistant

assistant = OfficeAssistant()

tests = [
    ("How many WFH days can I take?", "NC1001"),
    ("How many leave days do I have?", "NC1001"),
]

for query, emp_id in tests:
    print("=" * 60)
    print("Query:", query)

    state = assistant.process_query(
        user_query=query,
        employee_id=emp_id,
    )

    print("Intent:", state.intent)
    print("Route:", state.route)
    print("Tool:", state.tool_name)
    print("Response:", state.response)

    if state.citations:
        print("Citations:", len(state.citations))