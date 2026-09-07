"""
Intent definitions used across the NexaAssist application.
"""

from enum import Enum


class Intent(str, Enum):
    # RAG
    POLICY_QUERY = "policy_query"

    # MCP Tools
    EMPLOYEE_INFO = "employee_info"

    LEAVE_BALANCE = "leave_balance"
    LEAVE_REQUESTS = "leave_requests"
    SUBMIT_LEAVE = "submit_leave"

    EMPLOYEE_EXPENSES = "employee_expenses"
    EXPENSE_STATUS = "expense_status"
    SUBMIT_EMPLOYEE_EXPENSE = "submit_employee_expense"

    ASSIGNED_ASSETS = "assigned_assets"

    OFFICE_LOCATION = "office_location"

    # Fallback
    UNKNOWN = "unknown"