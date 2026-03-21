#!/bin/bash

# Script para iniciar o RouteCalc Pro em modo desenvolvimento

echo "🚀 Iniciando RouteCalc Pro - Modo Desenvolvimento"
echo "================================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Iniciar serviços de desenvolvimento
echo "📦 Iniciando serviços de desenvolvimento..."
docker-compose --profile dev up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ RouteCalc Pro (Desenvolvimento) iniciado com sucesso!"
    echo ""
    echo "🌐 Aplicações disponíveis:"
    echo "   • Frontend Dev: http://localhost:5002 (com hot reload)"
    echo "   • Backend API: http://localhost:5001 (com hot reload)"
    echo "   • API Docs: http://localhost:5001/docs"
    echo "   • PostgreSQL: localhost:5433"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   • Ver logs: docker-compose logs -f"
    echo "   • Parar: docker-compose down"
    echo "   • PgAdmin: docker-compose --profile admin up -d"
    echo ""
    echo "🔍 Verificando status dos serviços..."
    sleep 5
    docker-compose ps
else
    echo "❌ Erro ao iniciar os serviços"
    exit 1
fi
