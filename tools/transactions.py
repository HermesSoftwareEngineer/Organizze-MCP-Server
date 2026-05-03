import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_transaction_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_transactions(
        start_date: str,
        end_date: str,
        account_id: int | None = None,
    ) -> str:
        """Lista transações em um período.

        Args:
            start_date: Data inicial no formato YYYY-MM-DD.
            end_date: Data final no formato YYYY-MM-DD.
            account_id: Filtrar por conta bancária (opcional).
        """
        try:
            params: dict = {"start_date": start_date, "end_date": end_date}
            if account_id is not None:
                params["account_id"] = account_id
            result = await client.get("/transactions", params=params)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_transaction(id: int) -> str:
        """Retorna os detalhes de uma transação pelo ID."""
        try:
            result = await client.get(f"/transactions/{id}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_create_transaction(
        description: str,
        date: str,
        amount: int,
        account_id: int,
        paid: bool = True,
        category_id: int | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
        total_installments: int | None = None,
        recurrence_policy: str | None = None,
    ) -> str:
        """Cria uma transação (receita ou despesa).

        Args:
            description: Descrição da transação.
            date: Data no formato YYYY-MM-DD.
            amount: Valor em CENTAVOS. Negativo = despesa, positivo = receita
                    (ex: -5000 = despesa de R$50,00; 10000 = receita de R$100,00).
            account_id: ID da conta bancária.
            paid: Se a transação já foi paga/recebida.
            category_id: ID da categoria (opcional).
            notes: Observações (opcional).
            tags: Lista de tags (opcional).
            total_installments: Número de parcelas, para compras parceladas (opcional).
            recurrence_policy: Recorrência: 'no_repeat', 'weekly', 'biweekly',
                                'monthly' ou 'yearly' (opcional).
        """
        try:
            body: dict = {
                "description": description,
                "date": date,
                "amount_cents": amount,
                "account_id": account_id,
                "paid": paid,
            }
            if category_id is not None:
                body["category_id"] = category_id
            if notes is not None:
                body["notes"] = notes
            if tags is not None:
                body["tags"] = tags
            if total_installments is not None:
                body["total_installments"] = total_installments
            if recurrence_policy is not None:
                body["recurrence_policy"] = recurrence_policy
            result = await client.post("/transactions", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_update_transaction(
        id: int,
        description: str | None = None,
        date: str | None = None,
        amount: int | None = None,
        account_id: int | None = None,
        paid: bool | None = None,
        category_id: int | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Atualiza uma transação existente.

        Args:
            id: ID da transação.
            amount: Valor em CENTAVOS (negativo = despesa, positivo = receita).
            date: Data no formato YYYY-MM-DD.
        """
        try:
            body: dict = {}
            if description is not None:
                body["description"] = description
            if date is not None:
                body["date"] = date
            if amount is not None:
                body["amount_cents"] = amount
            if account_id is not None:
                body["account_id"] = account_id
            if paid is not None:
                body["paid"] = paid
            if category_id is not None:
                body["category_id"] = category_id
            if notes is not None:
                body["notes"] = notes
            if tags is not None:
                body["tags"] = tags
            result = await client.put(f"/transactions/{id}", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_delete_transaction(id: int) -> str:
        """Remove uma transação pelo ID."""
        try:
            await client.delete(f"/transactions/{id}")
            return f"Transação {id} removida com sucesso."
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
