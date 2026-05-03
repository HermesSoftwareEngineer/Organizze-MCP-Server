from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient
from tools.users import register_user_tools
from tools.accounts import register_account_tools
from tools.categories import register_category_tools
from tools.credit_cards import register_credit_card_tools
from tools.transactions import register_transaction_tools
from tools.transfers import register_transfer_tools
from tools.budgets import register_budget_tools


def register_all_tools(mcp: FastMCP, client: OrganizzeClient) -> None:
    register_user_tools(mcp, client)
    register_account_tools(mcp, client)
    register_category_tools(mcp, client)
    register_credit_card_tools(mcp, client)
    register_transaction_tools(mcp, client)
    register_transfer_tools(mcp, client)
    register_budget_tools(mcp, client)
