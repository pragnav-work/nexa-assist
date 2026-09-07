from src.models.intents import Intent

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


class ToolDispatcher:

    def __init__(self):
        self.registry = {
            Intent.EMPLOYEE_INFO: get_employee,
            Intent.LEAVE_BALANCE: get_leave_balance,
            Intent.LEAVE_REQUESTS: get_leave_requests,
            Intent.SUBMIT_LEAVE: apply_leave,
            Intent.EMPLOYEE_EXPENSES: get_expenses,
            Intent.EXPENSE_STATUS: get_expense_status,
            Intent.SUBMIT_EMPLOYEE_EXPENSE: submit_expense,
            Intent.ASSIGNED_ASSETS: get_assigned_assets,
            Intent.OFFICE_LOCATION: get_office_location,
        }

    def execute(self, intent: Intent, **kwargs):

        tool = self.registry.get(intent)

        if tool is None:
            return "Requested tool is not available."

        # Leave balance
        if intent == Intent.LEAVE_BALANCE:
            return tool(kwargs["employee_id"])

        # Leave requests
        elif intent == Intent.LEAVE_REQUESTS:
            return tool(kwargs["employee_id"])

        # Employee info
        elif intent == Intent.EMPLOYEE_INFO:
            return tool(kwargs["employee_id"])

        # Employee expenses
        elif intent == Intent.EMPLOYEE_EXPENSES:
            return tool(kwargs["employee_id"])

        # Assigned assets
        elif intent == Intent.ASSIGNED_ASSETS:
            return tool(kwargs["employee_id"])

        # Office location (this tool probably expects the query)
        elif intent == Intent.OFFICE_LOCATION:
            return tool(kwargs["query"])

        # Leave application / expense submission will need parameter extraction later
        else:
            return tool(**kwargs)