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

    employee_id = employee_id.strip().upper()
    expense_type_normalized = expense_type.strip().lower()
    description = description.strip()

    # Validate employee
    employees = read_csv("employees.csv")

    employee = employees[
        employees["employee_id"].astype(str).str.upper() == employee_id
    ]

    if employee.empty:
        return {
            "success": False,
            "message": f"Employee {employee_id} not found.",
        }

    # Validate expense type
    if expense_type_normalized not in VALID_EXPENSE_TYPES:
        return {
            "success": False,
            "message": "Invalid expense type.",
        }

    # Validate amount
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Expense amount must be a valid number.",
        }

    if amount <= 0:
        return {
            "success": False,
            "message": "Expense amount must be greater than zero.",
        }

    # Validate date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "success": False,
            "message": "Date must use YYYY-MM-DD format.",
        }

    # Validate description
    if not description:
        return {
            "success": False,
            "message": "Expense description cannot be empty.",
        }

    # Generate next expense ID
    expenses = read_csv("expense_records.csv")

    if expenses.empty:
        expense_id = "EX5001"
    else:
        existing_numbers = (
            expenses["expense_id"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .dropna()
            .astype(int)
        )

        next_number = existing_numbers.max() + 1
        expense_id = f"EX{next_number:04d}"

    record = {
        "expense_id": expense_id,
        "employee_id": employee_id,
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