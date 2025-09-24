#!/bin/bash

# Script para build e execução do backend com Docker

echo "🚀 Iniciando build do backend..."

# Build da imagem
echo "📦 Construindo imagem Docker do backend..."
docker build -t routecalc-backend .

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    
    # Parar containers existentes
    echo "🛑 Parando containers existentes..."
    docker-compose down
    
    # Executar com docker-compose
    echo "🏃 Iniciando serviços com docker-compose..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Serviços iniciados com sucesso!"
        echo "🌐 Backend disponível em: http://localhost:50001"
        echo "📊 API Docs disponível em: http://localhost:50001/docs"
        echo "🗄️ PostgreSQL disponível em: localhost:5432"
        echo ""
        echo "📋 Comandos úteis:"
        echo "  - Ver logs: docker-compose logs -f backend"
        echo "  - Parar serviços: docker-compose down"
        echo "  - Reiniciar: docker-compose restart backend"
    else
        echo "❌ Erro ao iniciar serviços"
        exit 1
    fi
else
    echo "❌ Erro no build da imagem"
    exit 1
fi
