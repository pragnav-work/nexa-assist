from src.tools.tool_dispatcher import ToolDispatcher
from src.models.intents import Intent

# Create dispatcher
dispatcher = ToolDispatcher()

# Temporary mock tools
dispatcher.registry = {
    "leave_balance": lambda **kwargs: "Leave Balance Tool Called",
    "employee_info": lambda **kwargs: "Employee Info Tool Called",
}

# Test
print(dispatcher.execute(Intent.LEAVE_BALANCE))
print(dispatcher.execute(Intent.EMPLOYEE_INFO))
print(dispatcher.execute(Intent.UNKNOWN))