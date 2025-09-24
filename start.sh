#!/bin/bash

# Script para iniciar o RouteCalc Pro completo

echo "🚀 Iniciando RouteCalc Pro - Sistema Completo"
echo "=============================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Build e iniciar todos os serviços
echo "📦 Construindo e iniciando todos os serviços..."
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ RouteCalc Pro iniciado com sucesso!"
    echo ""
    echo "🌐 Aplicações disponíveis:"
    echo "   • Frontend: http://localhost:5000"
    echo "   • Backend API: http://localhost:50001"
    echo "   • API Docs: http://localhost:50001/docs"
    echo "   • PostgreSQL: localhost:5432"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   • Ver logs: docker-compose logs -f"
    echo "   • Parar: docker-compose down"
    echo "   • Reiniciar: docker-compose restart"
    echo "   • PgAdmin: docker-compose --profile admin up -d"
    echo ""
    echo "🔍 Verificando status dos serviços..."
    sleep 5
    docker-compose ps
else
    echo "❌ Erro ao iniciar os serviços"
    exit 1
fi
