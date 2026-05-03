import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_budget_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_budgets() -> str:
        """Lista os orçamentos do mês atual no Organizze."""
        try:
            result = await client.get("/budgets")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_budgets_for_year(year: int) -> str:
        """Lista os orçamentos de um ano específico.

        Args:
            year: Ano com 4 dígitos (ex: 2025).
        """
        try:
            result = await client.get(f"/budgets/{year}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_budgets_for_month(year: int, month: int) -> str:
        """Lista os orçamentos de um mês específico.

        Args:
            year: Ano com 4 dígitos (ex: 2025).
            month: Mês de 1 a 12.
        """
        try:
            result = await client.get(f"/budgets/{year}/{month}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
