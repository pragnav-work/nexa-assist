from .csv_utils import read_csv


def get_employee(employee_id: str) -> dict:
    """Get employee information by employee ID."""

    employees = read_csv("employees.csv")

    employee = employees[
        employees["employee_id"].astype(str).str.upper() == employee_id.upper()
    ]

    if employee.empty:
        return {
            "success": False,
            "message": f"Employee {employee_id} not found."
        }

    return {
        "success": True,
        "employee": employee.iloc[0].to_dict()
    }