@echo off
REM Script para build e execução do backend com Docker no Windows

echo 🚀 Iniciando build do backend...

REM Build da imagem
echo 📦 Construindo imagem Docker do backend...
docker build -t routecalc-backend .

if %errorlevel% equ 0 (
    echo ✅ Build concluído com sucesso!
    
    REM Parar containers existentes
    echo 🛑 Parando containers existentes...
    docker-compose down
    
    REM Executar com docker-compose
    echo 🏃 Iniciando serviços com docker-compose...
    docker-compose up -d
    
    if %errorlevel% equ 0 (
        echo ✅ Serviços iniciados com sucesso!
        echo 🌐 Backend disponível em: http://localhost:8000
        echo 📊 API Docs disponível em: http://localhost:8000/docs
        echo 🗄️ PostgreSQL disponível em: localhost:5432
        echo.
        echo 📋 Comandos úteis:
        echo   - Ver logs: docker-compose logs -f backend
        echo   - Parar serviços: docker-compose down
        echo   - Reiniciar: docker-compose restart backend
    ) else (
        echo ❌ Erro ao iniciar serviços
        exit /b 1
    )
) else (
    echo ❌ Erro no build da imagem
    exit /b 1
)
