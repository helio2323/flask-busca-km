@echo off
REM Script para verificar e iniciar o Docker Desktop

echo 🔍 Verificando status do Docker Desktop...

REM Verificar se o Docker Desktop está rodando
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Desktop está rodando!
    echo.
    echo 🚀 Iniciando RouteCalc Pro...
    docker-compose up --build -d
) else (
    echo ❌ Docker Desktop não está rodando
    echo.
    echo 🔧 Tentando iniciar o Docker Desktop...
    
    REM Tentar iniciar o Docker Desktop
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo ⏳ Aguardando o Docker Desktop inicializar...
    echo    (Isso pode levar alguns minutos na primeira vez)
    echo.
    
    REM Aguardar o Docker Desktop inicializar
    :wait_loop
    timeout /t 10 /nobreak >nul
    docker info >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Docker Desktop iniciado com sucesso!
        echo.
        echo 🚀 Iniciando RouteCalc Pro...
        docker-compose up --build -d
    ) else (
        echo ⏳ Ainda aguardando o Docker Desktop...
        goto wait_loop
    )
)
