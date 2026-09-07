from datetime import date

from src.validation.validator import (
    validate_action_confirmation,
    validate_employee_context,
    validate_expense_submission,
    validate_it_request,
    validate_leave_request,
)


def test_valid_employee_context():
    result = validate_employee_context(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_wrong_employee_context():
    result = validate_employee_context(
        session_employee_id="NC1001",
        requested_employee_id="NC1002",
    )

    assert result["valid"] is False
    assert "current employee session" in result["errors"][0]


def test_valid_leave_request():
    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 12),
        requested_days=3,
        available_balance=10,
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_leave_exceeds_balance():
    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 20),
        requested_days=11,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "exceeds available balance" in result["errors"][0]


def test_invalid_leave_dates():
    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 20),
        end_date=date(2026, 9, 10),
        requested_days=5,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "Start date cannot be after end date." in result["errors"]


def test_missing_leave_type():
    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 12),
        requested_days=3,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "Leave type is required." in result["errors"]


def test_invalid_expense_amount():
    result = validate_expense_submission(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        expense_type="Travel",
        amount=0,
        expense_date=date(2026, 9, 3),
        description="Taxi expense",
    )

    assert result["valid"] is False
    assert "Expense amount must be greater than zero." in result["errors"]


def test_valid_it_request():
    result = validate_it_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        issue_description="Laptop is not connecting to Wi-Fi.",
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_confirmation_required():
    result = validate_action_confirmation(False)

    assert result["valid"] is False
    assert "confirmation is required" in result["errors"][0]


def test_confirmation_accepted():
    result = validate_action_confirmation(True)

    assert result["valid"] is True
    assert result["errors"] == []

def test_employee_cannot_access_another_employee_data():
    result = validate_employee_context(
        session_employee_id="NC1001",
        requested_employee_id="NC1002",
    )

    assert result["valid"] is False
    assert "current employee session" in result["errors"][0]
