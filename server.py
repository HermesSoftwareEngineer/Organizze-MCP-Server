import os
import sys
from pathlib import Path

# Garante que o diretório do script está no path (necessário quando executado pelo Claude Desktop)
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from client import OrganizzeClient
from tools import register_all_tools

load_dotenv()

_email = os.environ.get("ORGANIZZE_EMAIL")
_token = os.environ.get("ORGANIZZE_API_TOKEN")

if not _email or not _token:
    sys.stderr.write(
        "[organizze-mcp] FATAL: ORGANIZZE_EMAIL e ORGANIZZE_API_TOKEN devem estar definidos.\n"
    )
    sys.exit(1)

client = OrganizzeClient(_email, _token)
mcp = FastMCP("organizze-mcp-server")
register_all_tools(mcp, client)


class _BearerAuthMiddleware:
    """ASGI middleware que exige Authorization: Bearer <MCP_AUTH_TOKEN>."""

    def __init__(self, app, token: str) -> None:
        self.app = app
        self.token = token

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            auth = headers.get(b"authorization", b"").decode()
            if not auth.startswith("Bearer ") or auth[7:] != self.token:
                # Retorna 401 sem chamar o app
                await _unauthorized_response(scope, receive, send)
                return
        await self.app(scope, receive, send)


async def _unauthorized_response(scope, receive, send) -> None:
    await send({"type": "http.response.start", "status": 401, "headers": []})
    await send({"type": "http.response.body", "body": b"Unauthorized"})


def main() -> None:
    transport = os.environ.get("TRANSPORT", "stdio")

    if transport == "sse":
        import uvicorn

        port = int(os.environ.get("PORT", "8080"))
        auth_token = os.environ.get("MCP_AUTH_TOKEN")

        app = mcp.sse_app()
        if auth_token:
            app = _BearerAuthMiddleware(app, auth_token)

        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
