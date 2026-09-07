from src.tools.employee_tools import get_employee
from src.tools.leave_tools import (
    get_leave_balance,
    get_leave_requests,
)
from src.tools.expense_tools import (
    get_expenses,
    get_expense_status,
)
from src.tools.it_tools import get_assigned_assets
from src.tools.office_tools import get_office_location


def test_get_employee():
    result = get_employee("NC1001")

    assert result["success"] is True
    assert result["employee"]["employee_id"] == "NC1001"


def test_get_employee_not_found():
    result = get_employee("INVALID")

    assert result["success"] is False


def test_get_leave_balance():
    result = get_leave_balance("NC1001")

    assert result["success"] is True
    assert result["leave_balance"]["employee_id"] == "NC1001"


def test_get_leave_requests():
    result = get_leave_requests("NC1001")

    assert result["success"] is True
    assert isinstance(result["requests"], list)


def test_get_expenses():
    result = get_expenses("NC1001")

    assert result["success"] is True
    assert isinstance(result["expenses"], list)


def test_get_expense_status():
    result = get_expense_status("EX5001")

    assert result["success"] is True
    assert result["status"] == "Approved"


def test_expense_not_found():
    result = get_expense_status("INVALID")

    assert result["success"] is False


def test_get_assigned_assets():
    result = get_assigned_assets("NC1001")

    assert result["success"] is True
    assert isinstance(result["assets"], list)


def test_get_office_location():
    result = get_office_location("Chennai")

    assert result["success"] is True
    assert result["office"]["city"] == "Chennai"


def test_office_not_found():
    result = get_office_location("Delhi")

    assert result["success"] is False