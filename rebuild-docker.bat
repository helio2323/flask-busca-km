@echo off
REM Script para limpar e reconstruir containers com novas portas

echo 🧹 Limpando e reconstruindo containers com novas portas...
echo ========================================================

REM Parar todos os containers
echo 1. Parando containers existentes...
docker-compose down

REM Remover imagens antigas para forçar rebuild
echo 2. Removendo imagens antigas...
docker rmi routecalc-frontend 2>nul
docker rmi routecalc-backend 2>nul

REM Limpar cache do Docker
echo 3. Limpando cache do Docker...
docker system prune -f

REM Rebuild completo
echo 4. Reconstruindo com novas configurações...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ Rebuild concluído com sucesso!
    echo.
    echo 🌐 Aplicações disponíveis:
    echo    • Frontend: http://localhost:5000
    echo    • Backend: http://localhost:5001
    echo    • API Docs: http://localhost:5001/docs
    echo.
    echo 🔍 Verificando status...
    timeout /t 5 /nobreak >nul
    docker-compose ps
) else (
    echo ❌ Erro no rebuild
    exit /b 1
)
