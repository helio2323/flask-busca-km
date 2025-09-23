FROM python:3.11.6-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Definir diretório de trabalho
WORKDIR /FLASK-BUSCA-KM

# Copiar requirements primeiro para aproveitar cache de layers
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor a porta
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python3", "index.py"]
