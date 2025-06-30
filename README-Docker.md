# Flask Busca KM - Docker

Este projeto é uma aplicação web desenvolvida em Quart (Flask assíncrono) para calcular distâncias e pedágios entre cidades brasileiras.

## 🚀 Como usar com Docker

### Pré-requisitos

- Docker instalado
- Docker Compose (ou Docker com comando `compose`)

### Opção 1: Usando o script facilitador

```bash
# Tornar o script executável (se ainda não estiver)
chmod +x run-docker.sh

# Iniciar o projeto
./run-docker.sh start

# Ver logs
./run-docker.sh logs

# Parar o projeto
./run-docker.sh stop

# Outras opções
./run-docker.sh
```

### Opção 2: Usando Docker Compose diretamente

```bash
# Build da aplicação
docker compose build

# Iniciar em background
docker compose up -d

# Ver logs
docker compose logs -f flask-busca-km

# Parar
docker compose down
```

## 📱 Acessando a aplicação

Depois de iniciar, acesse: **http://localhost:5000**

## ⚙️ Funcionalidades

- ✅ Cálculo de distância entre cidades
- ✅ Cálculo de pedágios
- ✅ Upload de planilhas Excel
- ✅ Cache inteligente para otimizar consultas
- ✅ API REST para integração

## 🔧 Comandos úteis do script

| Comando | Descrição |
|---------|-----------|
| `start` ou `up` | Inicia o projeto |
| `stop` ou `down` | Para o projeto |
| `restart` | Reinicia o projeto |
| `logs` | Exibe os logs em tempo real |
| `build` | Reconstrói a imagem |
| `status` | Mostra status dos containers |
| `shell` | Acessa o shell do container |

## 📋 Exemplo de uso da API

```bash
# Calcular distância entre duas cidades
GET http://localhost:5000/km/São Paulo/Rio de Janeiro

# Upload de planilha Excel
POST http://localhost:5000/upload
```

## 🐛 Troubleshooting

- **Container não inicia**: Verifique se a porta 5000 não está em uso
- **Erro de build**: Execute `./run-docker.sh build` para refazer o build
- **Ver logs detalhados**: Use `./run-docker.sh logs` 