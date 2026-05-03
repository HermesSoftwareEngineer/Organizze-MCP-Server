import base64
import httpx
from typing import Any


BASE_URL = "https://api.organizze.com.br/rest/v2"


class OrganizzeApiError(Exception):
    def __init__(self, status: int, body: Any, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class OrganizzeClient:
    def __init__(self, email: str, token: str) -> None:
        credentials = base64.b64encode(f"{email}:{token}".encode()).decode()
        self._headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "User-Agent": f"OrganizzeMCP/1.0 ({email})",
        }

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        async with httpx.AsyncClient() as http:
            r = await http.request(
                method,
                f"{BASE_URL}{path}",
                headers=self._headers,
                params=params,
                json=json,
            )
        if r.status_code == 401:
            raise OrganizzeApiError(
                401,
                None,
                "Credenciais inválidas. Verifique ORGANIZZE_EMAIL e ORGANIZZE_API_TOKEN.",
            )
        if r.status_code == 422:
            body = r.json() if r.content else {}
            errors = body.get("errors", body) if isinstance(body, dict) else body
            raise OrganizzeApiError(422, body, f"Erro de validação: {errors}")
        if not r.is_success:
            raise OrganizzeApiError(
                r.status_code,
                None,
                f"HTTP {r.status_code}: {r.reason_phrase}",
            )
        return r.json() if r.content else None

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, body: Any) -> Any:
        return await self.request("POST", path, json=body)

    async def put(self, path: str, body: Any) -> Any:
        return await self.request("PUT", path, json=body)

    async def delete(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self.request("DELETE", path, params=params)
