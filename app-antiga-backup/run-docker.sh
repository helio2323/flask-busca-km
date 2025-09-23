#!/bin/bash

# Script para gerenciar o projeto Flask Busca KM com Docker

case "$1" in
    start|up)
        echo "🚀 Iniciando o projeto Flask Busca KM..."
        docker compose up -d
        echo "✅ Projeto iniciado! Acesse http://localhost:5000"
        ;;
    stop|down)
        echo "⏹️ Parando o projeto..."
        docker compose down
        echo "✅ Projeto parado!"
        ;;
    restart)
        echo "🔄 Reiniciando o projeto..."
        docker compose down
        docker compose up -d
        echo "✅ Projeto reiniciado! Acesse http://localhost:5000"
        ;;
    logs)
        echo "📋 Exibindo logs..."
        docker compose logs -f flask-busca-km
        ;;
    build)
        echo "🔨 Fazendo build da aplicação..."
        docker compose build --no-cache
        echo "✅ Build concluído!"
        ;;
    status)
        echo "📊 Status dos containers:"
        docker compose ps
        ;;
    shell)
        echo "🐚 Acessando shell do container..."
        docker compose exec flask-busca-km bash
        ;;
    *)
        echo "🔧 Uso: $0 {start|stop|restart|logs|build|status|shell}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start/up    - Inicia o projeto"
        echo "  stop/down   - Para o projeto"
        echo "  restart     - Reinicia o projeto"
        echo "  logs        - Exibe os logs"
        echo "  build       - Reconstrói a imagem"
        echo "  status      - Mostra status dos containers"
        echo "  shell       - Acessa o shell do container"
        exit 1
        ;;
esac 