import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_transfer_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_transfers() -> str:
        """Lista todas as transferências entre contas no Organizze."""
        try:
            result = await client.get("/transfers")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_transfer(id: int) -> str:
        """Retorna os detalhes de uma transferência pelo ID."""
        try:
            result = await client.get(f"/transfers/{id}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_create_transfer(
        amount: int,
        date: str,
        account_from_id: int,
        account_to_id: int,
        description: str | None = None,
        notes: str | None = None,
    ) -> str:
        """Cria uma transferência entre duas contas.

        Args:
            amount: Valor em CENTAVOS (ex: 50000 = R$500,00).
            date: Data no formato YYYY-MM-DD.
            account_from_id: ID da conta de origem.
            account_to_id: ID da conta de destino.
            description: Descrição da transferência (opcional).
            notes: Observações (opcional).
        """
        try:
            body: dict = {
                "amount_cents": amount,
                "date": date,
                "account_from_id": account_from_id,
                "account_to_id": account_to_id,
            }
            if description is not None:
                body["description"] = description
            if notes is not None:
                body["notes"] = notes
            result = await client.post("/transfers", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_update_transfer(
        id: int,
        amount: int | None = None,
        date: str | None = None,
        account_from_id: int | None = None,
        account_to_id: int | None = None,
        description: str | None = None,
        notes: str | None = None,
    ) -> str:
        """Atualiza uma transferência existente.

        Args:
            id: ID da transferência.
            amount: Valor em CENTAVOS (ex: 50000 = R$500,00).
            date: Data no formato YYYY-MM-DD.
        """
        try:
            body: dict = {}
            if amount is not None:
                body["amount_cents"] = amount
            if date is not None:
                body["date"] = date
            if account_from_id is not None:
                body["account_from_id"] = account_from_id
            if account_to_id is not None:
                body["account_to_id"] = account_to_id
            if description is not None:
                body["description"] = description
            if notes is not None:
                body["notes"] = notes
            result = await client.put(f"/transfers/{id}", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_delete_transfer(id: int) -> str:
        """Remove uma transferência pelo ID."""
        try:
            await client.delete(f"/transfers/{id}")
            return f"Transferência {id} removida com sucesso."
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
