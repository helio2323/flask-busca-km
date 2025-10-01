#!/bin/bash

echo "🚀 Iniciando sistema com Docker local..."

echo ""
echo "1. Parando containers existentes..."
docker compose -f docker-compose-local.yml down

echo ""
echo "2. Iniciando PostgreSQL..."
docker compose -f docker-compose-local.yml up postgres -d

echo ""
echo "3. Aguardando PostgreSQL inicializar..."
sleep 15

echo ""
echo "4. Verificando se PostgreSQL está rodando..."
docker ps | grep postgres

echo ""
echo "5. Iniciando Backend localmente..."
echo ""
echo "✅ Sistema iniciado!"
echo ""
echo "📍 URLs:"
echo "  - Backend API: http://localhost:8000"
echo "  - Documentação: http://localhost:8000/docs"
echo "  - PostgreSQL: localhost:5432"
echo "  - PgAdmin: http://localhost:5050 (admin@routecalc.com / admin)"
echo ""
echo "Para ver os logs do PostgreSQL:"
echo "docker logs -f routecalc-postgres"
echo ""
echo "Para parar o sistema:"
echo "docker compose -f docker-compose-local.yml down"
echo ""
echo "Pressione Ctrl+C para parar o backend"

cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
