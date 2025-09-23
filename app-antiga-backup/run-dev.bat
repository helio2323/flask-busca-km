@echo off
echo 🚀 Iniciando Sistema de Cálculo de Rotas - Desenvolvimento
echo ==================================================

REM Verificar se Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está rodando. Por favor, inicie o Docker primeiro.
    pause
    exit /b 1
)

REM Parar containers existentes
echo 🛑 Parando containers existentes...
docker-compose down

REM Construir e iniciar containers
echo 🔨 Construindo e iniciando containers...
docker-compose up --build -d

REM Aguardar PostgreSQL estar pronto
echo ⏳ Aguardando PostgreSQL estar pronto...
timeout /t 10 /nobreak >nul

REM Inicializar banco de dados
echo 🗄️ Inicializando banco de dados...
docker-compose exec backend python init_db.py

echo.
echo ✅ Sistema iniciado com sucesso!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 Documentação API: http://localhost:8000/docs
echo 🗄️ PostgreSQL: localhost:5432
echo.
echo Para parar o sistema: docker-compose down
echo Para ver logs: docker-compose logs -f
pause
