from src.tools.expense_tools import submit_expense
from src.tools.leave_tools import apply_leave


def test_invalid_employee_expense():
    result = submit_expense(
        "INVALID",
        "Meals",
        500,
        "2026-09-04",
        "Business lunch",
    )
    assert result["success"] is False


def test_invalid_expense_amount():
    result = submit_expense(
        "NC1001",
        "Meals",
        -100,
        "2026-09-04",
        "Business lunch",
    )
    assert result["success"] is False


def test_invalid_expense_date():
    result = submit_expense(
        "NC1001",
        "Meals",
        500,
        "04-09-2026",
        "Business lunch",
    )
    assert result["success"] is False


def test_invalid_leave_type():
    result = apply_leave(
        "NC1001",
        "Vacation Leave",
        "2026-09-10",
        "2026-09-11",
    )
    assert result["success"] is False


def test_invalid_leave_dates():
    result = apply_leave(
        "NC1001",
        "Casual Leave",
        "2026-09-15",
        "2026-09-10",
    )
    assert result["success"] is False


def test_submit_leave_success():
    result = apply_leave(
        "NC1001",
        "Casual Leave",
        "2026-12-15",
        "2026-12-16",
    )

    assert result["success"] is True
    assert result["request"]["employee_id"] == "NC1001"
    assert result["request"]["leave_type"] == "Casual Leave"
    assert result["request"]["days"] == 2
    assert result["request"]["status"] == "Pending"


def test_submit_expense_success():
    result = submit_expense(
        "NC1001",
        "Meals",
        1500,
        "2026-12-15",
        "Client business lunch",
    )

    assert result["success"] is True
    assert result["expense"]["employee_id"] == "NC1001"
    assert result["expense"]["expense_type"] == "Meals"
    assert result["expense"]["amount"] == 1500
    assert result["expense"]["status"] == "Pending"