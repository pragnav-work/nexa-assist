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

        # -------------------------------------------------
        # Read-only employee tools
        # -------------------------------------------------

        if intent == Intent.LEAVE_BALANCE:
            return tool(kwargs["employee_id"])

        elif intent == Intent.LEAVE_REQUESTS:
            return tool(kwargs["employee_id"])

        elif intent == Intent.EMPLOYEE_INFO:
            return tool(kwargs["employee_id"])

        elif intent == Intent.EMPLOYEE_EXPENSES:
            return tool(kwargs["employee_id"])

        elif intent == Intent.ASSIGNED_ASSETS:
            return tool(kwargs["employee_id"])

        elif intent == Intent.OFFICE_LOCATION:
            return tool(kwargs["query"])

        elif intent == Intent.EXPENSE_STATUS:
            return tool(kwargs["query"])

        # -------------------------------------------------
        # State-changing tools
        # -------------------------------------------------

        elif intent == Intent.SUBMIT_LEAVE:
            return tool(
                employee_id=kwargs["employee_id"],
                leave_type=kwargs["leave_type"],
                start_date=kwargs["start_date"],
                end_date=kwargs["end_date"],
            )

        elif intent == Intent.SUBMIT_EMPLOYEE_EXPENSE:
            return tool(
                employee_id=kwargs["employee_id"],
                expense_type=kwargs["expense_type"],
                amount=kwargs["amount"],
                expense_date=kwargs["expense_date"],
                description=kwargs["description"],
            )

        return "Requested tool is not available."
