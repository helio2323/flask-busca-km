@echo off
echo 🔧 Resolvendo problema de autenticação do Docker...

echo.
echo 1. Fazendo logout do Docker Hub...
docker logout

echo.
echo 2. Limpando cache do Docker...
docker system prune -f

echo.
echo 3. Tentando fazer login no Docker Hub...
echo Digite suas credenciais do Docker Hub quando solicitado:
docker login

echo.
echo 4. Testando pull das imagens base...
docker pull python:3.11-slim
docker pull node:18-alpine

echo.
echo 5. Executando Docker Compose...
docker compose up --build

pause
