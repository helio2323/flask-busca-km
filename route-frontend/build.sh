#!/bin/bash

# Script para build e execução do frontend com Docker

echo "🚀 Iniciando build do frontend..."

# Build da imagem
echo "📦 Construindo imagem Docker..."
docker build -t routecalc-frontend .

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    
    # Executar container
    echo "🏃 Iniciando container..."
    docker run -d \
        --name routecalc-frontend \
        -p 3000:3000 \
        -e NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 \
        routecalc-frontend
    
    if [ $? -eq 0 ]; then
        echo "✅ Container iniciado com sucesso!"
        echo "🌐 Aplicação disponível em: http://localhost:3000"
    else
        echo "❌ Erro ao iniciar container"
        exit 1
    fi
else
    echo "❌ Erro no build da imagem"
    exit 1
fi
