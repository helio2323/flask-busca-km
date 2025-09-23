# RouteCalc Pro - Backend Docker

Este diretório contém a API backend do RouteCalc Pro configurada para execução com Docker.

## 🐳 Arquivos Docker

- `Dockerfile` - Imagem de desenvolvimento com hot reload
- `Dockerfile.prod` - Imagem de produção otimizada
- `docker-compose.yml` - Orquestração dos serviços (PostgreSQL + Backend)
- `.dockerignore` - Arquivos ignorados no build
- `init_db.sql` - Script de inicialização do banco

## 🚀 Como Executar

### Opção 1: Docker Compose (Recomendado)

```bash
# Executar em desenvolvimento
docker-compose up -d

# Executar em produção
docker-compose --profile production up -d

# Executar com PgAdmin
docker-compose --profile admin up -d
```

### Opção 2: Docker Build Manual

```bash
# Build da imagem
docker build -t routecalc-backend .

# Executar apenas o backend (requer PostgreSQL externo)
docker run -d \
  --name routecalc-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  routecalc-backend
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

- `POSTGRES_DB` - Nome do banco de dados (padrão: rotas_db)
- `POSTGRES_USER` - Usuário do PostgreSQL (padrão: postgres)
- `POSTGRES_PASSWORD` - Senha do PostgreSQL (padrão: postgres)
- `DATABASE_URL` - URL completa do banco de dados
- `ENVIRONMENT` - Ambiente de execução (development/production)

### Portas

- **8000** - API Backend (desenvolvimento)
- **8001** - API Backend (produção)
- **5432** - PostgreSQL
- **5050** - PgAdmin (opcional)

## 📁 Estrutura

```
backend/
├── Dockerfile              # Imagem de desenvolvimento
├── Dockerfile.prod         # Imagem de produção
├── docker-compose.yml      # Orquestração
├── .dockerignore           # Arquivos ignorados
├── init_db.sql            # Inicialização do banco
├── env.example            # Exemplo de variáveis
├── build.sh               # Script de build (Linux/Mac)
├── build.bat              # Script de build (Windows)
└── README-Docker.md       # Este arquivo
```

## 🛠️ Comandos Úteis

```bash
# Ver logs do backend
docker-compose logs -f backend

# Ver logs do PostgreSQL
docker-compose logs -f postgres

# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reiniciar apenas o backend
docker-compose restart backend

# Acessar shell do backend
docker-compose exec backend bash

# Acessar shell do PostgreSQL
docker-compose exec postgres psql -U postgres -d rotas_db

# Rebuild da imagem
docker-compose build --no-cache backend
```

## 🔍 Troubleshooting

### Backend não conecta ao banco
- Verifique se o PostgreSQL está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs postgres`
- Aguarde o health check do PostgreSQL completar

### Erro de permissão
- Verifique se o usuário tem permissão para acessar o Docker
- Execute: `sudo usermod -aG docker $USER` (Linux)

### Porta já em uso
- Verifique se a porta 8000 ou 5432 estão livres
- Mude as portas no docker-compose.yml se necessário

### Problemas de build
- Limpe o cache: `docker system prune -a`
- Rebuild sem cache: `docker-compose build --no-cache`

## 📊 Monitoramento

### Health Checks
- Backend: `http://localhost:8000/health`
- PostgreSQL: Verificado automaticamente pelo Docker

### Logs
- Backend: `docker-compose logs -f backend`
- PostgreSQL: `docker-compose logs -f postgres`

### PgAdmin (Opcional)
- URL: `http://localhost:5050`
- Email: `admin@routecalc.com`
- Senha: `admin`
