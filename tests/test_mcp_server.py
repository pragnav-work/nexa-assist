import sys
from pathlib import Path

import pytest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.asyncio
async def test_mcp_server_tools():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.mcp.server"],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.list_tools()

            tool_names = {
                tool.name
                for tool in result.tools
            }

            expected_tools = {
                "employee_info",
                "leave_balance",
                "leave_requests",
                "submit_leave",
                "employee_expenses",
                "expense_status",
                "submit_employee_expense",
                "assigned_assets",
                "office_location",
            }

            assert expected_tools.issubset(tool_names)