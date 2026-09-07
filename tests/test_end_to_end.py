from datetime import date

from src.validation.validator import (
    validate_employee_context,
    validate_leave_request,
    validate_action_confirmation,
)


def test_end_to_end_blocks_cross_employee_access():
    """Another employee's data must not be accessible."""

    result = validate_employee_context(
        session_employee_id="NC1001",
        requested_employee_id="NC1002",
    )

    assert result["valid"] is False
    assert result["errors"]


def test_end_to_end_blocks_leave_exceeding_balance():
    """A leave request exceeding the available balance must be rejected."""

    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 24),
        requested_days=15,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "exceeds available balance" in result["errors"][0]


def test_end_to_end_valid_leave_requires_confirmation():
    """A valid leave request must still require explicit confirmation."""

    leave_result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 12),
        requested_days=3,
        available_balance=10,
    )

    assert leave_result["valid"] is True

    confirmation_result = validate_action_confirmation(False)

    assert confirmation_result["valid"] is False
    assert "confirmation is required" in confirmation_result["errors"][0]


def test_end_to_end_confirmed_leave_can_proceed():
    """A valid leave request can proceed after explicit confirmation."""

    leave_result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 12),
        requested_days=3,
        available_balance=10,
    )

    assert leave_result["valid"] is True

    confirmation_result = validate_action_confirmation(True)

    assert confirmation_result["valid"] is True
    assert confirmation_result["errors"] == []


def test_end_to_end_past_leave_date_is_blocked():
    """A leave request starting in the past must be rejected."""

    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
        requested_days=2,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "cannot be in the past" in result["errors"][0]


def test_end_to_end_invalid_leave_dates_are_blocked():
    """A leave request with an invalid date range must be rejected."""

    result = validate_leave_request(
        session_employee_id="NC1001",
        requested_employee_id="NC1001",
        leave_type="earned_leave",
        start_date=date(2026, 9, 15),
        end_date=date(2026, 9, 10),
        requested_days=5,
        available_balance=10,
    )

    assert result["valid"] is False
    assert "cannot be after" in result["errors"][0]


def test_end_to_end_missing_leave_type_is_blocked():
    """A leave request without a leave type must be rejected."""

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
