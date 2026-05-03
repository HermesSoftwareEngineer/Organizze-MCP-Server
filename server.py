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

_transport = os.environ.get("TRANSPORT", "stdio")
_port = int(os.environ.get("PORT", "8080"))

# Para SSE/Streamable HTTP/Cloud Run: desabilita DNS rebinding protection e configura host/port.
_mcp_kwargs: dict = {}
if _transport in ("sse", "streamable-http"):
    _mcp_kwargs = {
        "host": "0.0.0.0",
        "port": _port,
        "transport_security": {"enable_dns_rebinding_protection": False},
    }

client = OrganizzeClient(_email, _token)
mcp = FastMCP("organizze-mcp-server", **_mcp_kwargs)
register_all_tools(mcp, client)


class _TokenAuthMiddleware:
    """ASGI middleware: aceita token via Authorization: Bearer <token> ou ?token=<token>."""

    def __init__(self, app, token: str) -> None:
        self.app = app
        self.token = token

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] in ("http", "websocket"):
            # Tenta header Authorization
            headers = dict(scope.get("headers", []))
            auth = headers.get(b"authorization", b"").decode()
            if auth.startswith("Bearer ") and auth[7:] == self.token:
                await self.app(scope, receive, send)
                return
            # Tenta query param ?token=
            query = scope.get("query_string", b"").decode()
            params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
            if params.get("token") == self.token:
                await self.app(scope, receive, send)
                return
            await _unauthorized_response(scope, receive, send)
        else:
            await self.app(scope, receive, send)


async def _unauthorized_response(scope, receive, send) -> None:
    await send({"type": "http.response.start", "status": 401, "headers": []})
    await send({"type": "http.response.body", "body": b"Unauthorized"})


def main() -> None:
    if _transport in ("sse", "streamable-http"):
        import uvicorn

        auth_token = os.environ.get("MCP_AUTH_TOKEN")

        if _transport == "streamable-http":
            app = mcp.streamable_http_app()
        else:
            app = mcp.sse_app()

        if auth_token:
            app = _TokenAuthMiddleware(app, auth_token)

        uvicorn.run(app, host="0.0.0.0", port=_port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
