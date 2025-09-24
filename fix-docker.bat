@echo off
REM Script para diagnosticar e corrigir problemas do Docker Desktop

echo 🔧 RouteCalc Pro - Diagnóstico e Correção do Docker
echo ==================================================

echo.
echo 🔍 Verificando status do Docker Desktop...

REM Verificar se Docker está rodando
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Desktop está funcionando!
    goto :start_system
) else (
    echo ❌ Docker Desktop não está funcionando
    goto :fix_docker
)

:fix_docker
echo.
echo 🔧 Tentando corrigir problemas do Docker Desktop...

REM Parar todos os processos do Docker
echo 🛑 Parando processos do Docker...
taskkill /F /IM "Docker Desktop.exe" 2>nul
taskkill /F /IM "com.docker.backend.exe" 2>nul
taskkill /F /IM "com.docker.proxy.exe" 2>nul

REM Aguardar um pouco
echo ⏳ Aguardando processos pararem...
timeout /t 5 /nobreak >nul

REM Limpar containers órfãos
echo 🧹 Limpando containers órfãos...
docker system prune -f 2>nul

REM Reiniciar Docker Desktop
echo 🚀 Reiniciando Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo ⏳ Aguardando Docker Desktop inicializar...
echo    (Isso pode levar 2-3 minutos)

REM Aguardar Docker inicializar
:wait_docker
timeout /t 15 /nobreak >nul
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Desktop iniciado com sucesso!
    goto :start_system
) else (
    echo ⏳ Ainda aguardando... (tentativa %counter%)
    set /a counter+=1
    if %counter% gtr 20 (
        echo ❌ Timeout: Docker Desktop não conseguiu inicializar
        echo.
        echo 💡 Soluções manuais:
        echo    1. Reinicie o computador
        echo    2. Reinstale o Docker Desktop
        echo    3. Verifique se a virtualização está habilitada no BIOS
        pause
        exit /b 1
    )
    goto :wait_docker
)

:start_system
echo.
echo 🚀 Iniciando RouteCalc Pro...

REM Parar containers existentes
echo 🛑 Parando containers existentes...
docker-compose down 2>nul

REM Iniciar sistema
echo 📦 Construindo e iniciando todos os serviços...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ RouteCalc Pro iniciado com sucesso!
    echo.
    echo 🌐 Aplicações disponíveis:
    echo    • Frontend: http://localhost:5000
    echo    • Backend API: http://localhost:50001
    echo    • API Docs: http://localhost:50001/docs
    echo    • PostgreSQL: localhost:5432
    echo.
    echo 📋 Comandos úteis:
    echo    • Ver logs: docker-compose logs -f
    echo    • Parar: docker-compose down
    echo    • Status: docker-compose ps
    echo.
    echo 🔍 Verificando status dos serviços...
    timeout /t 5 /nobreak >nul
    docker-compose ps
) else (
    echo ❌ Erro ao iniciar o sistema
    echo.
    echo 🔍 Verificando logs de erro...
    docker-compose logs
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul
