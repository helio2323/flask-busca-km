@echo off
REM Script para iniciar o RouteCalc Pro completo no Windows

echo 🚀 Iniciando RouteCalc Pro - Sistema Completo
echo ==============================================

REM Verificar se Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está rodando. Por favor, inicie o Docker Desktop.
    exit /b 1
)

REM Parar containers existentes
echo 🛑 Parando containers existentes...
docker-compose down

REM Build e iniciar todos os serviços
echo 📦 Construindo e iniciando todos os serviços...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ RouteCalc Pro iniciado com sucesso!
    echo.
    echo 🌐 Aplicações disponíveis:
    echo    • Frontend: http://localhost:3000
    echo    • Backend API: http://localhost:8000
    echo    • API Docs: http://localhost:8000/docs
    echo    • PostgreSQL: localhost:5432
    echo.
    echo 📋 Comandos úteis:
    echo    • Ver logs: docker-compose logs -f
    echo    • Parar: docker-compose down
    echo    • Reiniciar: docker-compose restart
    echo    • PgAdmin: docker-compose --profile admin up -d
    echo.
    echo 🔍 Verificando status dos serviços...
    timeout /t 5 /nobreak >nul
    docker-compose ps
) else (
    echo ❌ Erro ao iniciar os serviços
    exit /b 1
)
