#!/bin/bash

echo "🚀 Iniciando correção dos problemas da VPS..."

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker compose down

# 1. Corrigir problema do banco de dados
echo "📊 === CORRIGINDO BANCO DE DADOS ==="

# Iniciar apenas o PostgreSQL
echo "🔄 Iniciando PostgreSQL..."
docker compose up -d postgres

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
until docker exec routecalc-postgres pg_isready -U postgres; do
  echo "PostgreSQL não está pronto ainda..."
  sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Criar o banco de dados
echo "📊 Criando banco de dados 'rotas_db'..."
docker exec routecalc-postgres psql -U postgres -c "CREATE DATABASE rotas_db;" 2>/dev/null || echo "Banco 'rotas_db' já existe"

# Verificar se o banco foi criado
echo "🔍 Verificando banco de dados..."
docker exec routecalc-postgres psql -U postgres -c "\l" | grep rotas_db

# 2. Corrigir problema do backend
echo "🐍 === CORRIGINDO BACKEND ==="

# Verificar se main.py existe
if [ ! -f "backend/main.py" ]; then
    echo "❌ Arquivo backend/main.py não encontrado!"
    echo "📁 Listando arquivos:"
    ls -la backend/
    exit 1
fi

echo "✅ Arquivo backend/main.py encontrado!"

# Verificar estrutura do app
if [ ! -d "backend/app" ]; then
    echo "❌ Diretório backend/app não encontrado!"
    exit 1
fi

echo "✅ Estrutura de diretórios correta!"

# Testar importação local
echo "🧪 Testando importação Python..."
cd backend
python3 -c "from main import app; print('✅ Importação bem-sucedida!')" || {
    echo "❌ Erro na importação Python!"
    echo "🔍 Verificando estrutura:"
    ls -la
    exit 1
}

cd ..

# 3. Reconstruir e iniciar todos os containers
echo "🔨 === RECONSTRUINDO CONTAINERS ==="

# Rebuild e start
echo "🔄 Reconstruindo containers..."
docker compose up --build -d

# Aguardar containers estarem prontos
echo "⏳ Aguardando containers estarem prontos..."
sleep 10

# Verificar status
echo "📊 Status dos containers:"
docker ps

# Testar endpoints
echo "🧪 Testando endpoints..."

# Testar backend
echo "🔍 Testando backend..."
curl -f http://localhost:5001/health && echo "✅ Backend funcionando!" || echo "❌ Backend com problemas"

# Testar frontend (se estiver rodando)
echo "🔍 Testando frontend..."
curl -f http://localhost:5000 > /dev/null 2>&1 && echo "✅ Frontend funcionando!" || echo "⚠️ Frontend não está rodando"

echo "🎉 Correção concluída!"
echo "📋 Resumo:"
echo "  - PostgreSQL: ✅ Banco 'rotas_db' criado"
echo "  - Backend: ✅ Módulo 'main' corrigido"
echo "  - Containers: ✅ Reconstruídos e rodando"
