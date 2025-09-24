@echo off
REM Script para iniciar o RouteCalc Pro em modo desenvolvimento no Windows

echo 🚀 Iniciando RouteCalc Pro - Modo Desenvolvimento
echo =================================================

REM Verificar se Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está rodando. Por favor, inicie o Docker Desktop.
    exit /b 1
)

REM Parar containers existentes
echo 🛑 Parando containers existentes...
docker-compose down

REM Iniciar serviços de desenvolvimento
echo 📦 Iniciando serviços de desenvolvimento...
docker-compose --profile dev up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ RouteCalc Pro (Desenvolvimento) iniciado com sucesso!
    echo.
    echo 🌐 Aplicações disponíveis:
    echo    • Frontend Dev: http://localhost:3001 (com hot reload)
    echo    • Backend API: http://localhost:50001 (com hot reload)
    echo    • API Docs: http://localhost:50001/docs
    echo    • PostgreSQL: localhost:5432
    echo.
    echo 📋 Comandos úteis:
    echo    • Ver logs: docker-compose logs -f
    echo    • Parar: docker-compose down
    echo    • PgAdmin: docker-compose --profile admin up -d
    echo.
    echo 🔍 Verificando status dos serviços...
    timeout /t 5 /nobreak >nul
    docker-compose ps
) else (
    echo ❌ Erro ao iniciar os serviços
    exit /b 1
)
