#!/bin/bash

echo "🧹 Limpando e reconstruindo containers com novas portas..."
echo "========================================================"

# Parar todos os containers
echo "1. Parando containers existentes..."
docker-compose down

# Remover imagens antigas para forçar rebuild
echo "2. Removendo imagens antigas..."
docker rmi $(docker images -q routecalc-frontend) 2>/dev/null || true
docker rmi $(docker images -q routecalc-backend) 2>/dev/null || true

# Limpar cache do Docker
echo "3. Limpando cache do Docker..."
docker system prune -f

# Rebuild completo
echo "4. Reconstruindo com novas configurações..."
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Rebuild concluído com sucesso!"
    echo ""
    echo "🌐 Aplicações disponíveis:"
    echo "   • Frontend: http://localhost:5000"
    echo "   • Backend: http://localhost:5001"
    echo "   • API Docs: http://localhost:5001/docs"
    echo ""
    echo "🔍 Verificando status..."
    sleep 5
    docker-compose ps
else
    echo "❌ Erro no rebuild"
    exit 1
fi
