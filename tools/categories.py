import json
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient, OrganizzeApiError


def register_category_tools(mcp: FastMCP, client: OrganizzeClient) -> None:

    @mcp.tool()
    async def organizze_list_categories() -> str:
        """Lista todas as categorias de transações do Organizze."""
        try:
            result = await client.get("/categories")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_get_category(id: int) -> str:
        """Retorna os detalhes de uma categoria pelo ID."""
        try:
            result = await client.get(f"/categories/{id}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_create_category(
        name: str,
        color: str = "#ffffff",
        parent_id: int | None = None,
    ) -> str:
        """Cria uma categoria de transação.

        Args:
            name: Nome da categoria.
            color: Cor em formato hexadecimal (ex: '#ff5733').
            parent_id: ID da categoria pai para criar uma subcategoria.
        """
        try:
            body: dict = {"name": name, "color": color}
            if parent_id is not None:
                body["parent_id"] = parent_id
            result = await client.post("/categories", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_update_category(
        id: int,
        name: str | None = None,
        color: str | None = None,
    ) -> str:
        """Atualiza uma categoria existente.

        Args:
            id: ID da categoria.
            color: Cor em formato hexadecimal (ex: '#ff5733').
        """
        try:
            body: dict = {}
            if name is not None:
                body["name"] = name
            if color is not None:
                body["color"] = color
            result = await client.put(f"/categories/{id}", body)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"

    @mcp.tool()
    async def organizze_delete_category(
        id: int,
        replacement_id: int | None = None,
    ) -> str:
        """Remove uma categoria pelo ID.

        Args:
            id: ID da categoria a remover.
            replacement_id: Se informado, as transações desta categoria são movidas
                            para esta outra categoria antes da exclusão.
        """
        try:
            params = {"replacement_id": replacement_id} if replacement_id is not None else None
            await client.delete(f"/categories/{id}", params=params)
            return f"Categoria {id} removida com sucesso."
        except OrganizzeApiError as e:
            return f"Erro [{e.status}]: {e}"
