from datetime import datetime

from .csv_utils import read_csv, append_csv


VALID_LEAVE_TYPES = {
    "casual leave",
    "earned leave",
    "sick leave",
}


def get_leave_balance(employee_id: str) -> dict:
    """Get an employee's leave balance."""

    balances = read_csv("leave_balance.csv")

    result = balances[
        balances["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    if result.empty:
        return {
            "success": False,
            "message": f"Leave balance not found for {employee_id}."
        }

    return {
        "success": True,
        "leave_balance": result.iloc[0].to_dict()
    }


def get_leave_requests(employee_id: str) -> dict:
    """Get leave requests submitted by an employee."""

    requests = read_csv("leave_requests.csv")

    result = requests[
        requests["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    return {
        "success": True,
        "requests": result.to_dict(orient="records")
    }


def apply_leave(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
) -> dict:
    """Submit a new leave request."""

    leave_type_normalized = leave_type.strip().lower()

    if leave_type_normalized not in VALID_LEAVE_TYPES:
        return {
            "success": False,
            "message": "Invalid leave type."
        }

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {
            "success": False,
            "message": "Dates must use YYYY-MM-DD format."
        }

    if end < start:
        return {
            "success": False,
            "message": "End date cannot be before start date."
        }

    # Verify employee exists
    balances = read_csv("leave_balance.csv")

    employee = balances[
        balances["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    if employee.empty:
        return {
            "success": False,
            "message": f"Employee {employee_id} not found."
        }

    # Calculate calendar days for the demo
    days = (end - start).days + 1

    column_map = {
        "casual leave": "casual_leave",
        "earned leave": "earned_leave",
        "sick leave": "sick_leave",
    }

    balance_column = column_map[leave_type_normalized]
    available = int(employee.iloc[0][balance_column])

    if days > available:
        return {
            "success": False,
            "message": (
                f"Insufficient leave balance. "
                f"Available: {available}, requested: {days}."
            )
        }

    # Generate a simple request ID
    existing_requests = read_csv("leave_requests.csv")

    if existing_requests.empty:
        request_id = "LR7001"
    else:
        existing_numbers = (
            existing_requests["request_id"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .dropna()
            .astype(int)
        )

        next_number = existing_numbers.max() + 1
        request_id = f"LR{next_number:04d}"

    record = {
        "request_id": request_id,
        "employee_id": employee_id.upper(),
        "leave_type": leave_type.title(),
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    append_csv("leave_requests.csv", record)

    return {
        "success": True,
        "message": "Leave request submitted successfully.",
        "request": record,
    }