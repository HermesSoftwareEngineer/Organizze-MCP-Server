import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_user_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_get_current_user() -> str:
        """Retorna os dados do usuário autenticado no Organizze."""
        try:
            result = await client.get("/users")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
