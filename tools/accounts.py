import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_account_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_accounts() -> str:
        """Lista todas as contas bancárias cadastradas no Organizze."""
        try:
            result = await client.get("/accounts")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_account(id: int) -> str:
        """Retorna os detalhes de uma conta bancária pelo ID."""
        try:
            result = await client.get(f"/accounts/{id}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_create_account(
        name: str,
        balance: int,
        account_type: str = "checking",
        default: bool = False,
        archived: bool = False,
    ) -> str:
        """Cria uma conta bancária.

        Args:
            name: Nome da conta.
            balance: Saldo inicial em CENTAVOS (ex: 100000 = R$1.000,00).
            account_type: Tipo da conta: 'checking', 'savings' ou 'other'.
            default: Se deve ser a conta padrão.
            archived: Se a conta está arquivada.
        """
        try:
            body = {
                "name": name,
                "balance": balance,
                "type": account_type,
                "default": default,
                "archived": archived,
            }
            result = await client.post("/accounts", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_update_account(
        id: int,
        name: str | None = None,
        balance: int | None = None,
        account_type: str | None = None,
        default: bool | None = None,
        archived: bool | None = None,
    ) -> str:
        """Atualiza uma conta bancária existente.

        Args:
            id: ID da conta.
            balance: Saldo em CENTAVOS (ex: 100000 = R$1.000,00).
        """
        try:
            body: dict = {}
            if name is not None:
                body["name"] = name
            if balance is not None:
                body["balance"] = balance
            if account_type is not None:
                body["type"] = account_type
            if default is not None:
                body["default"] = default
            if archived is not None:
                body["archived"] = archived
            result = await client.put(f"/accounts/{id}", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_delete_account(id: int) -> str:
        """Remove uma conta bancária pelo ID."""
        try:
            await client.delete(f"/accounts/{id}")
            return f"Conta {id} removida com sucesso."
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
