from src.agents.office_assistant import OfficeAssistant

assistant = OfficeAssistant()

chat_history = []

# First question
'''query1 = "Tell me about the business travel policy."

state = assistant.process_query(
    user_query=query1,
    employee_id="NC1001",
    chat_history=chat_history,
)

print("Q1:", query1)
print("A1:", state.response)

# Store the first user message
chat_history.append(query1)

print("-" * 50)'''

# Follow-up question
query2 = "What is the reimbursement limit?"

state = assistant.process_query(
    user_query=query2,
    employee_id="NC1001",
    chat_history=chat_history,
)

print("Q2:", query2)
print("A2:", state.response)