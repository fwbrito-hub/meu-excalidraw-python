# 1. Imagem base
FROM python:3.13-slim

# 2. Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 3. Instalação de dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalação de dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Cópia do código fonte
COPY . .

# 6. Exposição da porta
EXPOSE 8000

# 7. Comando de inicialização
# Usamos shell form para garantir que a variável $PORT do Railway seja expandida
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
