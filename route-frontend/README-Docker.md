# RouteCalc Pro - Frontend Docker

Este diretório contém a aplicação frontend do RouteCalc Pro configurada para execução com Docker.

## 🐳 Arquivos Docker

- `Dockerfile` - Imagem de produção otimizada
- `Dockerfile.dev` - Imagem para desenvolvimento
- `docker-compose.yml` - Orquestração dos serviços
- `.dockerignore` - Arquivos ignorados no build

## 🚀 Como Executar

### Opção 1: Docker Compose (Recomendado)

```bash
# Executar em produção
docker-compose up -d

# Executar em modo desenvolvimento
docker-compose --profile dev up -d frontend-dev
```

### Opção 2: Docker Build Manual

```bash
# Build da imagem
docker build -t routecalc-frontend .

# Executar container
docker run -d \
  --name routecalc-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 \
  routecalc-frontend
```

### Opção 3: Scripts Automatizados

**Windows:**
```cmd
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

## 🔧 Configurações

### Variáveis de Ambiente

- `NEXT_PUBLIC_API_URL` - URL da API backend (padrão: http://localhost:8000/api/v1)
- `NODE_ENV` - Ambiente de execução (production/development)

### Portas

- **3000** - Aplicação frontend (produção)
- **3001** - Aplicação frontend (desenvolvimento)

## 📁 Estrutura

```
route-frontend/
├── Dockerfile              # Imagem de produção
├── Dockerfile.dev          # Imagem de desenvolvimento
├── docker-compose.yml      # Orquestração
├── .dockerignore           # Arquivos ignorados
├── build.sh               # Script de build (Linux/Mac)
├── build.bat              # Script de build (Windows)
├── env.example            # Exemplo de variáveis
└── README-Docker.md       # Este arquivo
```

## 🛠️ Comandos Úteis

```bash
# Ver logs do container
docker logs routecalc-frontend

# Parar container
docker stop routecalc-frontend

# Remover container
docker rm routecalc-frontend

# Acessar shell do container
docker exec -it routecalc-frontend sh

# Rebuild da imagem
docker build --no-cache -t routecalc-frontend .
```

## 🔍 Troubleshooting

### Container não inicia
- Verifique se a porta 3000 está livre
- Verifique os logs: `docker logs routecalc-frontend`

### Erro de build
- Limpe o cache: `docker system prune -a`
- Rebuild sem cache: `docker build --no-cache -t routecalc-frontend .`

### Problemas de conectividade com API
- Verifique se o backend está rodando na porta 8000
- Ajuste a variável `NEXT_PUBLIC_API_URL` se necessário
