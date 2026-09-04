from datetime import datetime

from .csv_utils import read_csv, append_csv


VALID_EXPENSE_TYPES = {
    "travel",
    "meals",
    "office supplies",
    "professional event",
}


def get_expenses(employee_id: str) -> dict:
    """Get all expense records for an employee."""

    expenses = read_csv("expense_records.csv")

    result = expenses[
        expenses["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    return {
        "success": True,
        "expenses": result.to_dict(orient="records"),
    }


def get_expense_status(expense_id: str) -> dict:
    """Get the status of a specific expense."""

    expenses = read_csv("expense_records.csv")

    result = expenses[
        expenses["expense_id"].astype(str).str.upper() == expense_id.upper()
    ]

    if result.empty:
        return {
            "success": False,
            "message": f"Expense {expense_id} not found.",
        }

    record = result.iloc[0].to_dict()

    return {
        "success": True,
        "expense_id": expense_id.upper(),
        "status": record["status"],
        "expense": record,
    }


def submit_expense(
    employee_id: str,
    expense_type: str,
    amount: float,
    date: str,
    description: str,
) -> dict:
    """Submit a new expense for reimbursement."""

    expense_type_normalized = expense_type.strip().lower()

    if expense_type_normalized not in VALID_EXPENSE_TYPES:
        return {
            "success": False,
            "message": (
                "Invalid expense type. "
                "Allowed types: Travel, Meals, Office Supplies, "
                "Professional Event."
            ),
        }

    if amount <= 0:
        return {
            "success": False,
            "message": "Expense amount must be greater than zero.",
        }

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "success": False,
            "message": "Date must use YYYY-MM-DD format.",
        }

    # Verify employee exists
    employees = read_csv("employees.csv")

    employee = employees[
        employees["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    if employee.empty:
        return {
            "success": False,
            "message": f"Employee {employee_id} not found.",
        }

    expenses = read_csv("expense_records.csv")

    if expenses.empty:
        expense_id = "EX5001"
    else:
        expense_id = f"EX{5001 + len(expenses):04d}"

    record = {
        "expense_id": expense_id,
        "employee_id": employee_id.upper(),
        "expense_type": expense_type.title(),
        "amount": amount,
        "date": date,
        "status": "Pending",
        "description": description,
    }

    append_csv("expense_records.csv", record)

    return {
        "success": True,
        "message": "Expense submitted successfully.",
        "expense": record,
    }