@echo off
REM Script para build e execução do frontend com Docker no Windows

echo 🚀 Iniciando build do frontend...

REM Build da imagem
echo 📦 Construindo imagem Docker...
docker build -t routecalc-frontend .

if %errorlevel% equ 0 (
    echo ✅ Build concluído com sucesso!
    
    REM Parar container existente se houver
    docker stop routecalc-frontend 2>nul
    docker rm routecalc-frontend 2>nul
    
    REM Executar container
    echo 🏃 Iniciando container...
    docker run -d ^
        --name routecalc-frontend ^
        -p 3000:3000 ^
        -e NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 ^
        routecalc-frontend
    
    if %errorlevel% equ 0 (
        echo ✅ Container iniciado com sucesso!
        echo 🌐 Aplicação disponível em: http://localhost:3000
    ) else (
        echo ❌ Erro ao iniciar container
        exit /b 1
    )
) else (
    echo ❌ Erro no build da imagem
    exit /b 1
)
