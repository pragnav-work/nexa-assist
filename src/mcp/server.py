from mcp.server.fastmcp import FastMCP

from src.tools.employee_tools import get_employee

from src.tools.leave_tools import (
    get_leave_balance,
    get_leave_requests,
    apply_leave,
)

from src.tools.expense_tools import (
    get_expenses,
    get_expense_status,
    submit_expense,
)

from src.tools.it_tools import get_assigned_assets
from src.tools.office_tools import get_office_location


mcp = FastMCP("NexaAssist")


# -------------------------
# Employee
# -------------------------

@mcp.tool()
def employee_info(employee_id: str) -> dict:
    """Get employee information."""
    return get_employee(employee_id)


# -------------------------
# Leave
# -------------------------

@mcp.tool()
def leave_balance(employee_id: str) -> dict:
    """Get an employee's available leave balance."""
    return get_leave_balance(employee_id)


@mcp.tool()
def leave_requests(employee_id: str) -> dict:
    """Get an employee's leave request history."""
    return get_leave_requests(employee_id)


@mcp.tool()
def submit_leave(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
) -> dict:
    """Submit a new employee leave request."""

    return apply_leave(
        employee_id,
        leave_type,
        start_date,
        end_date,
    )


# -------------------------
# Expenses
# -------------------------

@mcp.tool()
def employee_expenses(employee_id: str) -> dict:
    """Get expense records for an employee."""
    return get_expenses(employee_id)


@mcp.tool()
def expense_status(expense_id: str) -> dict:
    """Get the status of an expense."""
    return get_expense_status(expense_id)


@mcp.tool()
def submit_employee_expense(
    employee_id: str,
    expense_type: str,
    amount: float,
    date: str,
    description: str,
) -> dict:
    """Submit a new employee expense."""

    return submit_expense(
        employee_id,
        expense_type,
        amount,
        date,
        description,
    )


# -------------------------
# IT Assets
# -------------------------

@mcp.tool()
def assigned_assets(employee_id: str) -> dict:
    """Get IT assets assigned to an employee."""
    return get_assigned_assets(employee_id)


# -------------------------
# Office
# -------------------------

@mcp.tool()
def office_location(city: str) -> dict:
    """Get NexaCore office information for a city."""
    return get_office_location(city)


if __name__ == "__main__":
    mcp.run()