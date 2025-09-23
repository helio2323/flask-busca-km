#!/bin/bash

echo "🚀 Iniciando Sistema de Cálculo de Rotas - Desenvolvimento"
echo "=================================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar containers
echo "🔨 Construindo e iniciando containers..."
docker-compose up --build -d

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
sleep 10

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
docker-compose exec backend python init_db.py

echo ""
echo "✅ Sistema iniciado com sucesso!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 Documentação API: http://localhost:8000/docs"
echo "🗄️ PostgreSQL: localhost:5432"
echo ""
echo "Para parar o sistema: docker-compose down"
echo "Para ver logs: docker-compose logs -f"
