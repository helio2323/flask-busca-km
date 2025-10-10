#!/bin/bash

echo "🔧 Corrigindo problemas do banco de dados..."

# Aguardar o PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
until pg_isready -h localhost -p 5432 -U postgres; do
  echo "PostgreSQL não está pronto ainda..."
  sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Criar o banco de dados se não existir
echo "📊 Criando banco de dados 'rotas_db'..."
psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE rotas_db;" 2>/dev/null || echo "Banco 'rotas_db' já existe ou erro ao criar"

# Verificar se o banco foi criado
echo "🔍 Verificando se o banco foi criado..."
psql -h localhost -p 5432 -U postgres -c "\l" | grep rotas_db

echo "✅ Configuração do banco concluída!"
