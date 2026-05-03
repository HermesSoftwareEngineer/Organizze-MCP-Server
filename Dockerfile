FROM python:3.12-slim

WORKDIR /app

# Instala dependências antes de copiar o código (aproveita cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY client.py server.py ./
COPY tools/ tools/

# Cloud Run injeta PORT automaticamente; SSE é o transporte remoto
ENV TRANSPORT=sse

EXPOSE 8080

CMD ["python", "server.py"]
