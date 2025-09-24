# Dockerfile para Backend FastAPI
FROM python:3.11-slim AS base

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para logs
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 50001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50001/health || exit 1

# Comando para executar a aplicação
CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "50001", "--reload"]