# RouteCalc Pro - Sistema Completo com Docker

Sistema completo de cálculo de rotas e pedágios com frontend Next.js, backend FastAPI e banco PostgreSQL, tudo orquestrado com Docker.

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   PostgreSQL    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Database)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Início Rápido

### Pré-requisitos
- Docker Desktop instalado e rodando
- Git (opcional)

### Executar o Sistema Completo

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Modo Desenvolvimento

**Windows:**
```cmd
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

## 🌐 Aplicações Disponíveis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:3000 | Interface principal da aplicação |
| **Backend API** | http://localhost:8000 | API REST do sistema |
| **API Docs** | http://localhost:8000/docs | Documentação interativa da API |
| **PostgreSQL** | localhost:5432 | Banco de dados |
| **PgAdmin** | http://localhost:5050 | Interface de gerenciamento do banco |

## 📁 Estrutura do Projeto

```
flask-busca-km/
├── docker-compose.yml          # Orquestração principal
├── env.example                 # Exemplo de variáveis de ambiente
├── start.sh / start.bat        # Scripts de inicialização
├── start-dev.sh / start-dev.bat # Scripts de desenvolvimento
├── README-Docker-Complete.md   # Este arquivo
├── backend/                    # API Backend
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── ...
└── route-frontend/             # Frontend Next.js
    ├── Dockerfile
    ├── docker-compose.yml
    └── ...
```

## 🛠️ Comandos Docker

### Comandos Básicos

```bash
# Iniciar todos os serviços
docker-compose up -d

# Iniciar com rebuild
docker-compose up --build -d

# Parar todos os serviços
docker-compose down

# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Comandos de Desenvolvimento

```bash
# Iniciar em modo desenvolvimento
docker-compose --profile dev up -d

# Iniciar com PgAdmin
docker-compose --profile admin up -d

# Reiniciar um serviço específico
docker-compose restart backend
docker-compose restart frontend

# Acessar shell de um container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Comandos de Manutenção

```bash
# Limpar volumes e containers
docker-compose down -v

# Rebuild sem cache
docker-compose build --no-cache

# Ver status dos containers
docker-compose ps

# Ver uso de recursos
docker stats
```

## 🔧 Configurações

### Variáveis de Ambiente

Copie o arquivo `env.example` para `.env` e ajuste as configurações:

```bash
cp env.example .env
```

Principais variáveis:
- `POSTGRES_DB` - Nome do banco de dados
- `POSTGRES_USER` - Usuário do PostgreSQL
- `POSTGRES_PASSWORD` - Senha do PostgreSQL
- `NEXT_PUBLIC_API_URL` - URL da API para o frontend

### Perfis de Execução

- **Produção**: `docker-compose up -d` (frontend otimizado)
- **Desenvolvimento**: `docker-compose --profile dev up -d` (hot reload)
- **Admin**: `docker-compose --profile admin up -d` (com PgAdmin)

## 🔍 Troubleshooting

### Problemas Comuns

**1. Porta já em uso**
```bash
# Verificar portas em uso
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432

# Parar processos que usam as portas
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5432 | xargs kill -9
```

**2. Containers não iniciam**
```bash
# Ver logs detalhados
docker-compose logs

# Limpar e rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

**3. Problemas de conectividade**
```bash
# Verificar rede Docker
docker network ls
docker network inspect flask-busca-km_routecalc-network

# Testar conectividade entre containers
docker-compose exec frontend ping backend
docker-compose exec backend ping postgres
```

**4. Problemas de permissão (Linux)**
```bash
# Dar permissão aos scripts
chmod +x start.sh start-dev.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# (Reiniciar sessão após executar)
```

### Logs e Debugging

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Acessar container para debug
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 📊 Monitoramento

### Health Checks
- Backend: `curl http://localhost:8000/health`
- Frontend: `curl http://localhost:3000`
- PostgreSQL: Verificado automaticamente pelo Docker

### Métricas
```bash
# Uso de recursos
docker stats

# Espaço em disco
docker system df

# Limpeza de recursos não utilizados
docker system prune -a
```

## 🚀 Deploy

### Produção
```bash
# Build para produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Com variáveis de ambiente específicas
POSTGRES_PASSWORD=senha_segura docker-compose up -d
```

### Desenvolvimento
```bash
# Modo desenvolvimento com hot reload
docker-compose --profile dev up -d
```

## 📚 Documentação Adicional

- [Backend Docker](./backend/README-Docker.md)
- [Frontend Docker](./route-frontend/README-Docker.md)
- [API Documentation](http://localhost:8000/docs) (quando rodando)

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
