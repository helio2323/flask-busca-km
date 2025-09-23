#!/bin/bash

# Script para gerenciar o projeto Flask Busca KM localmente (sem Docker)

VENV_PATH="venv/bin/activate"
PID_FILE=".flask_pid"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null; then
                echo "⚠️ Projeto já está rodando (PID: $PID)"
                echo "✅ Acesse http://localhost:5000"
                exit 0
            else
                rm "$PID_FILE"
            fi
        fi
        
        echo "🚀 Iniciando o projeto Flask Busca KM localmente..."
        
        if [ ! -d "venv" ]; then
            echo "❌ Ambiente virtual não encontrado. Execute: python -m venv venv"
            exit 1
        fi
        
        source "$VENV_PATH"
        nohup python index.py > flask.log 2>&1 &
        echo $! > "$PID_FILE"
        sleep 2
        
        if ps -p $(cat "$PID_FILE") > /dev/null; then
            echo "✅ Projeto iniciado! Acesse http://localhost:5000"
            echo "📋 Logs em: flask.log"
        else
            echo "❌ Erro ao iniciar o projeto. Verifique flask.log"
            rm "$PID_FILE"
        fi
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null; then
                echo "⏹️ Parando o projeto..."
                kill $PID
                rm "$PID_FILE"
                echo "✅ Projeto parado!"
            else
                echo "⚠️ Processo não encontrado"
                rm "$PID_FILE"
            fi
        else
            echo "⚠️ Projeto não está rodando"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null; then
                echo "✅ Projeto rodando (PID: $PID)"
                echo "🌐 URL: http://localhost:5000"
            else
                echo "❌ Projeto não está rodando"
                rm "$PID_FILE"
            fi
        else
            echo "❌ Projeto não está rodando"
        fi
        ;;
    logs)
        if [ -f "flask.log" ]; then
            echo "📋 Exibindo logs..."
            tail -f flask.log
        else
            echo "❌ Arquivo de log não encontrado"
        fi
        ;;
    install)
        echo "📦 Instalando dependências..."
        if [ ! -d "venv" ]; then
            echo "🔧 Criando ambiente virtual..."
            python -m venv venv
        fi
        source "$VENV_PATH"
        pip install -r requirements.txt
        echo "✅ Dependências instaladas!"
        ;;
    *)
        echo "🔧 Uso: $0 {start|stop|restart|status|logs|install}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start     - Inicia o projeto"
        echo "  stop      - Para o projeto"
        echo "  restart   - Reinicia o projeto"
        echo "  status    - Mostra status"
        echo "  logs      - Exibe logs em tempo real"
        echo "  install   - Instala dependências"
        exit 1
        ;;
esac 