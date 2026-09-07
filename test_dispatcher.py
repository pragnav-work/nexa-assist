from src.tools.tool_dispatcher import ToolDispatcher
from src.models.intents import Intent


dispatcher = ToolDispatcher()

# Temporary mock tools
dispatcher.registry = {
    Intent.LEAVE_BALANCE: lambda employee_id: "Leave Balance Tool Called",
    Intent.EMPLOYEE_INFO: lambda employee_id: "Employee Info Tool Called",
}


def test_leave_balance_dispatch():
    result = dispatcher.execute(
        Intent.LEAVE_BALANCE,
        employee_id="NC1001",
    )
    assert result == "Leave Balance Tool Called"


def test_employee_info_dispatch():
    result = dispatcher.execute(
        Intent.EMPLOYEE_INFO,
        employee_id="NC1001",
    )
    assert result == "Employee Info Tool Called"


def test_unknown_intent_dispatch():
    result = dispatcher.execute(Intent.UNKNOWN)
    assert result == "Requested tool is not available."
