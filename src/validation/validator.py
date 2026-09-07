from datetime import date


def validate_employee_context(
    session_employee_id: str,
    requested_employee_id: str,
) -> dict:
    """
    Ensures that the employee requesting information
    matches the employee represented by the current session.
    """

    if not session_employee_id:
        return {
            "valid": False,
            "errors": ["No employee session is active."],
            "warnings": [],
        }

    if not requested_employee_id:
        return {
            "valid": False,
            "errors": ["Employee ID is required."],
            "warnings": [],
        }

    if session_employee_id != requested_employee_id:
        return {
            "valid": False,
            "errors": [
                "You can only access information for the current employee session."
            ],
            "warnings": [],
        }

    return {
        "valid": True,
        "errors": [],
        "warnings": [],
    }


def validate_leave_request(
    session_employee_id: str,
    requested_employee_id: str,
    leave_type: str,
    start_date: date,
    end_date: date,
    requested_days: int,
    available_balance: int,
) -> dict:
    """
    Performs deterministic validation of a leave request.
    """

    errors = []
    warnings = []

    # Employee identity check
    employee_result = validate_employee_context(
        session_employee_id,
        requested_employee_id,
    )

    # Date validation
    if not start_date or not end_date:
        errors.append("Start date and end date are required.")
    elif start_date > end_date:
        errors.append("Start date cannot be after end date.")
    elif start_date < date.today():
        errors.append("Leave start date cannot be in the past.")    
    if not employee_result["valid"]:
            errors.extend(employee_result["errors"])

    # Required field
    if not leave_type:
        errors.append("Leave type is required.")

    # Date validation
    if not start_date or not end_date:
        errors.append("Start date and end date are required.")
    elif start_date > end_date:
        errors.append("Start date cannot be after end date.")

    # Days validation
    if requested_days <= 0:
        errors.append("Requested leave days must be greater than zero.")

    # Balance validation
    if requested_days > available_balance:
        errors.append("Requested leave exceeds available balance.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_expense_submission(
    session_employee_id: str,
    requested_employee_id: str,
    expense_type: str,
    amount: float,
    expense_date: date,
    description: str,
) -> dict:
    """
    Performs deterministic validation of an expense submission.
    """

    errors = []
    warnings = []

    employee_result = validate_employee_context(
        session_employee_id,
        requested_employee_id,
    )

    if not employee_result["valid"]:
        errors.extend(employee_result["errors"])

    if not expense_type:
        errors.append("Expense type is required.")

    if amount <= 0:
        errors.append("Expense amount must be greater than zero.")

    if not expense_date:
        errors.append("Expense date is required.")

    if not description:
        errors.append("Expense description is required.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_it_request(
    session_employee_id: str,
    requested_employee_id: str,
    issue_description: str,
) -> dict:
    """
    Performs deterministic validation of an IT request.
    """

    errors = []
    warnings = []

    employee_result = validate_employee_context(
        session_employee_id,
        requested_employee_id,
    )

    if not employee_result["valid"]:
        errors.extend(employee_result["errors"])

    if not issue_description:
        errors.append("IT issue description is required.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_action_confirmation(confirmed: bool) -> dict:
    """
    Ensures that a state-changing action has explicit
    user confirmation before execution.
    """

    if not confirmed:
        return {
            "valid": False,
            "errors": ["User confirmation is required before performing this action."],
            "warnings": [],
        }

    return {
        "valid": True,
        "errors": [],
        "warnings": [],
    }
