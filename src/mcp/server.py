from mcp.server.fastmcp import FastMCP

from src.tools.employee_tools import get_employee
from src.tools.leave_tools import (
    get_leave_balance,
    get_leave_requests,
    apply_leave,
)


mcp = FastMCP("NexaAssist")


@mcp.tool()
def employee_info(employee_id: str) -> dict:
    """Get employee information."""
    return get_employee(employee_id)


@mcp.tool()
def leave_balance(employee_id: str) -> dict:
    """Get the employee's available leave balance."""
    return get_leave_balance(employee_id)


@mcp.tool()
def leave_requests(employee_id: str) -> dict:
    """Get the employee's leave request history."""
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


if __name__ == "__main__":
    mcp.run()