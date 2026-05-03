import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_credit_card_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_credit_cards() -> str:
        """Lista todos os cartões de crédito cadastrados no Organizze."""
        try:
            result = await client.get("/credit_cards")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_credit_card(id: int) -> str:
        """Retorna os detalhes de um cartão de crédito pelo ID."""
        try:
            result = await client.get(f"/credit_cards/{id}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_create_credit_card(
        name: str,
        limit: int,
        closing_day: int,
        due_day: int,
        card_network: str = "visa",
        default: bool = False,
        archived: bool = False,
    ) -> str:
        """Cria um cartão de crédito.

        Args:
            name: Nome do cartão.
            limit: Limite em CENTAVOS (ex: 500000 = R$5.000,00).
            closing_day: Dia de fechamento da fatura (1-31).
            due_day: Dia de vencimento da fatura (1-31).
            card_network: Bandeira do cartão: 'visa', 'mastercard', 'amex', etc.
            default: Se é o cartão padrão.
            archived: Se está arquivado.
        """
        try:
            body = {
                "name": name,
                "limit_cents": limit,
                "closing_day": closing_day,
                "due_day": due_day,
                "card_network": card_network,
                "default": default,
                "archived": archived,
            }
            result = await client.post("/credit_cards", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_update_credit_card(
        id: int,
        name: str | None = None,
        limit: int | None = None,
        closing_day: int | None = None,
        due_day: int | None = None,
        card_network: str | None = None,
        default: bool | None = None,
        archived: bool | None = None,
    ) -> str:
        """Atualiza um cartão de crédito existente.

        Args:
            id: ID do cartão.
            limit: Limite em CENTAVOS (ex: 500000 = R$5.000,00).
        """
        try:
            body: dict = {}
            if name is not None:
                body["name"] = name
            if limit is not None:
                body["limit_cents"] = limit
            if closing_day is not None:
                body["closing_day"] = closing_day
            if due_day is not None:
                body["due_day"] = due_day
            if card_network is not None:
                body["card_network"] = card_network
            if default is not None:
                body["default"] = default
            if archived is not None:
                body["archived"] = archived
            result = await client.put(f"/credit_cards/{id}", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_delete_credit_card(id: int) -> str:
        """Remove um cartão de crédito pelo ID."""
        try:
            await client.delete(f"/credit_cards/{id}")
            return f"Cartão {id} removido com sucesso."
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_list_credit_card_invoices(
        credit_card_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Lista as faturas de um cartão de crédito.

        Args:
            credit_card_id: ID do cartão de crédito.
            start_date: Data inicial no formato YYYY-MM-DD (opcional).
            end_date: Data final no formato YYYY-MM-DD (opcional).
        """
        try:
            params: dict = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            result = await client.get(
                f"/credit_cards/{credit_card_id}/invoices",
                params=params or None,
            )
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_credit_card_invoice(
        credit_card_id: int,
        invoice_id: int,
    ) -> str:
        """Retorna os detalhes de uma fatura específica do cartão de crédito."""
        try:
            result = await client.get(
                f"/credit_cards/{credit_card_id}/invoices/{invoice_id}"
            )
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_pay_credit_card_invoice(
        credit_card_id: int,
        invoice_id: int,
        account_id: int,
        amount: int,
        date: str,
    ) -> str:
        """Registra o pagamento de uma fatura do cartão de crédito.

        Args:
            credit_card_id: ID do cartão de crédito.
            invoice_id: ID da fatura.
            account_id: ID da conta bancária de onde sai o pagamento.
            amount: Valor do pagamento em CENTAVOS (ex: 100000 = R$1.000,00).
            date: Data do pagamento no formato YYYY-MM-DD.
        """
        try:
            body = {
                "account_id": account_id,
                "amount_cents": amount,
                "date": date,
            }
            result = await client.post(
                f"/credit_cards/{credit_card_id}/invoices/{invoice_id}/payments",
                body,
            )
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
