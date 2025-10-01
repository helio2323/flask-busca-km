#!/bin/bash

echo "🚀 Iniciando sistema com backend local..."

echo ""
echo "1. Parando containers existentes..."
docker compose -f docker-compose-simple.yml down

echo ""
echo "2. Iniciando apenas PostgreSQL..."
docker compose -f docker-compose-simple.yml up postgres -d

echo ""
echo "3. Aguardando PostgreSQL inicializar..."
sleep 15

echo ""
echo "4. Verificando se PostgreSQL está rodando..."
docker ps | grep postgres

echo ""
echo "5. Instalando dependências Python localmente..."
cd backend
pip install -r requirements.txt

echo ""
echo "6. Iniciando Backend localmente..."
echo ""
echo "✅ Sistema iniciado!"
echo ""
echo "📍 URLs:"
echo "  - Backend API: http://localhost:8000"
echo "  - Documentação: http://localhost:8000/docs"
echo "  - PostgreSQL: localhost:5432"
echo ""
echo "Para parar o PostgreSQL:"
echo "docker compose -f docker-compose-simple.yml down"
echo ""
echo "Pressione Ctrl+C para parar o backend"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
