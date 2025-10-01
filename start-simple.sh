#!/bin/bash

echo "🚀 Iniciando sistema de forma simplificada..."

echo ""
echo "1. Parando containers existentes..."
docker compose -f docker-compose-simple.yml down

echo ""
echo "2. Iniciando PostgreSQL..."
docker compose -f docker-compose-simple.yml up postgres -d

echo ""
echo "3. Aguardando PostgreSQL inicializar..."
sleep 10

echo ""
echo "4. Iniciando Backend..."
docker compose -f docker-compose-simple.yml up backend -d

echo ""
echo "5. Verificando status dos containers..."
docker ps

echo ""
echo "✅ Sistema iniciado!"
echo ""
echo "📍 URLs:"
echo "  - Backend API: http://localhost:50001"
echo "  - Documentação: http://localhost:50001/docs"
echo "  - PostgreSQL: localhost:5432"
echo ""
echo "Para ver os logs do backend:"
echo "docker logs -f routecalc-backend"
echo ""
echo "Para parar o sistema:"
echo "docker compose -f docker-compose-simple.yml down"
