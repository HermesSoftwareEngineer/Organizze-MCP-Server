# Organizze MCP Server

MCP Server para a API do [Organizze](https://www.organizze.com.br), permitindo que o Claude Desktop acesse e gerencie suas finanças pessoais via linguagem natural.

## Funcionalidades

33 tools cobrindo toda a API do Organizze:

| Recurso | Tools disponíveis |
|---|---|
| Usuário | Consultar perfil autenticado |
| Contas | Listar, criar, editar, excluir |
| Categorias | Listar, criar, editar, excluir (com reassociação de transações) |
| Cartões de crédito | Listar, criar, editar, excluir, faturas, pagamento de fatura |
| Transações | Listar por período, criar, editar, excluir |
| Transferências | Listar, criar, editar, excluir |
| Orçamentos | Consultar por mês ou ano |

## Pré-requisitos

- Python 3.11+
- Conta no Organizze com token de API gerado em [configuracoes/api-keys](https://app.organizze.com.br/configuracoes/api-keys)

## Instalação local

```bash
git clone https://github.com/HermesSoftwareEngineer/Organizze-MCP-Server.git
cd Organizze-MCP-Server

python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# source .venv/bin/activate && pip install -r requirements.txt  # macOS/Linux

cp .env.example .env
# edite .env com suas credenciais
```

## Configuração

```env
ORGANIZZE_EMAIL=seu@email.com
ORGANIZZE_API_TOKEN=seu_token_aqui

# 'stdio' para Claude Desktop local | 'sse' para Cloud Run / remoto
TRANSPORT=stdio

# Necessário apenas no modo SSE — protege o endpoint com bearer token
# Gere com: python -c "import secrets; print(secrets.token_hex(32))"
MCP_AUTH_TOKEN=
```

## Uso

### Claude Desktop (local)

Edite `%APPDATA%\Claude\claude_desktop_config.json` (Windows) ou `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "organizze": {
      "command": "C:\\caminho\\para\\Organizze-MCP-Server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\caminho\\para\\Organizze-MCP-Server\\server.py"],
      "env": {
        "ORGANIZZE_EMAIL": "seu@email.com",
        "ORGANIZZE_API_TOKEN": "seu_token_aqui"
      }
    }
  }
}
```

Reinicie o Claude Desktop. As tools `organizze_*` estarão disponíveis.

### Testando interativamente

```bash
.venv/Scripts/mcp dev server.py
```

Abre uma interface web para chamar as tools manualmente e inspecionar respostas.

## Deploy no Google Cloud Run

### 1. Build e push da imagem

```bash
gcloud builds submit --tag gcr.io/SEU_PROJETO/organizze-mcp
```

### 2. Gere o token de autenticação

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Deploy

```bash
gcloud run deploy organizze-mcp \
  --image gcr.io/SEU_PROJETO/organizze-mcp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "ORGANIZZE_EMAIL=seu@email.com,ORGANIZZE_API_TOKEN=seu_token" \
  --set-env-vars "MCP_AUTH_TOKEN=token_gerado_acima"
```

> **Recomendado:** use o Secret Manager para não expor credenciais no histórico do terminal:
> ```bash
> gcloud secrets create ORGANIZZE_API_TOKEN --data-file=-  # cola o token e pressiona Ctrl+D
> gcloud run deploy organizze-mcp ... --set-secrets "ORGANIZZE_API_TOKEN=ORGANIZZE_API_TOKEN:latest"
> ```

### 4. Configure o Claude Desktop para o servidor remoto

```json
{
  "mcpServers": {
    "organizze": {
      "url": "https://organizze-mcp-xxxx.run.app/sse",
      "headers": {
        "Authorization": "Bearer token_gerado_acima"
      }
    }
  }
}
```

## Estrutura do projeto

```
├── server.py          # Entry point — detecta TRANSPORT e sobe stdio ou SSE
├── client.py          # Cliente HTTP da API do Organizze (Basic Auth)
├── tools/
│   ├── __init__.py    # Registra todas as tools no FastMCP
│   ├── accounts.py
│   ├── budgets.py
│   ├── categories.py
│   ├── credit_cards.py
│   ├── transactions.py
│   ├── transfers.py
│   └── users.py
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Exemplos de uso no Claude

> "Liste todas as minhas contas bancárias"

> "Quais foram meus gastos em março de 2025?"

> "Cria uma despesa de R$45,90 no restaurante hoje, categoria Alimentação"

> "Qual é o limite do meu cartão Nubank?"

> "Quanto sobrou do meu orçamento de lazer esse mês?"
