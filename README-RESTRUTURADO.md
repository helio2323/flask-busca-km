# Sistema de Cálculo de Rotas - Versão Reestruturada

## 🚀 Visão Geral

Sistema moderno para cálculo de distâncias e pedágios entre cidades brasileiras, com interface web responsiva e API RESTful.

## 🏗️ Arquitetura

### Backend (FastAPI + PostgreSQL)
- **API RESTful** com FastAPI
- **Banco de dados** PostgreSQL
- **Sistema de cache** inteligente
- **Integração** com API Rotas Brasil
- **Geocodificação** com Nominatim

### Frontend (Next.js + React)
- **Interface moderna** com Next.js 14
- **Componentes** reutilizáveis com Radix UI
- **Estilização** com Tailwind CSS
- **TypeScript** para tipagem estática

## 📁 Estrutura do Projeto

```
flask-busca-km/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints da API
│   │   ├── core/              # Configurações
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negócio
│   │   └── utils/             # Utilitários
│   ├── requirements.txt
│   ├── Dockerfile
│   └── init_db.py
├── route-frontend/            # Frontend Next.js
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
├── docker-compose.yml
├── run-dev.bat               # Script Windows
├── run-dev.sh                # Script Linux/Mac
└── README-RESTRUTURADO.md
```

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local do frontend)

### Execução com Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone <repository-url>
cd flask-busca-km
```

2. **Execute o script de desenvolvimento**
```bash
# Windows
run-dev.bat

# Linux/Mac
chmod +x run-dev.sh
./run-dev.sh
```

3. **Acesse as aplicações**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Execução Manual

1. **Backend**
```bash
cd backend
pip install -r requirements.txt
python init_db.py  # Inicializar banco
uvicorn app.main:app --reload
```

2. **Frontend**
```bash
cd route-frontend
npm install
npm run dev
```

3. **PostgreSQL**
```bash
# Usar Docker
docker run --name postgres-rotas -e POSTGRES_DB=rotas_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

## 📚 API Endpoints

### Rotas
- `POST /api/v1/routes/calculate` - Calcular rota individual
- `POST /api/v1/routes/calculate-multiple` - Calcular rota múltipla
- `POST /api/v1/routes/upload` - Upload de planilha Excel
- `GET /api/v1/routes/km/{origem}/{destino}` - Endpoint compatível

### Histórico
- `GET /api/v1/history` - Listar histórico de consultas
- `DELETE /api/v1/history/{id}` - Deletar consulta
- `DELETE /api/v1/history` - Limpar histórico

### Sugestões
- `GET /api/v1/suggestions/{termo}` - Sugestões de cidades

### Grupos
- `GET /api/v1/groups` - Listar grupos
- `POST /api/v1/groups` - Criar grupo
- `PUT /api/v1/groups/{id}` - Atualizar grupo
- `DELETE /api/v1/groups/{id}` - Deletar grupo

### Cache
- `GET /api/v1/cache/stats` - Estatísticas do cache
- `POST /api/v1/cache/clear` - Limpar cache

## 🗄️ Banco de Dados

### Tabelas Principais

- **consultas**: Histórico de consultas de rotas
- **grupos**: Grupos de rotas para organização
- **cache_coordenadas**: Cache de coordenadas geográficas
- **cache_rotas**: Cache de resultados de rotas

### Schema
```sql
-- Consultas
CREATE TABLE consultas (
    id SERIAL PRIMARY KEY,
    origem VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    distancia DECIMAL(10,2),
    pedagios DECIMAL(10,2),
    ip_address VARCHAR(45),
    data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_consulta VARCHAR(20) DEFAULT 'individual',
    grupo_id INTEGER REFERENCES grupos(id)
);

-- Grupos
CREATE TABLE grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Funcionalidades

### Calculadora de Rotas
- ✅ Cálculo de distância e pedágios
- ✅ Rotas individuais e múltiplas
- ✅ Integração com API Rotas Brasil
- ✅ Sistema de cache inteligente
- ✅ Geocodificação automática

### Upload de Planilhas
- ✅ Upload de arquivos Excel (.xlsx, .xls)
- ✅ Processamento em lote
- ✅ Validação de formato
- ✅ Organização por grupos

### Histórico de Consultas
- ✅ Visualização de consultas anteriores
- ✅ Filtros por tipo e grupo
- ✅ Estatísticas de uso
- ✅ Exportação de dados

### Gerenciamento de Grupos
- ✅ Criação e edição de grupos
- ✅ Organização de rotas
- ✅ Filtros por grupo

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para PostgreSQL
- **PostgreSQL** - Banco de dados principal
- **Pydantic** - Validação de dados
- **Geopy** - Geocodificação
- **Pandas** - Processamento de planilhas

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Radix UI** - Componentes acessíveis
- **Lucide React** - Ícones

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **PostgreSQL** - Banco de dados

## 🔄 Migração da Versão Anterior

### O que foi mantido
- ✅ **Funções de cálculo** de KM e pedágio (reutilizadas)
- ✅ **Integração** com API Rotas Brasil
- ✅ **Sistema de cache** (melhorado)
- ✅ **Geocodificação** com Nominatim
- ✅ **Upload de planilhas** Excel

### O que foi melhorado
- 🔄 **Arquitetura** separada (Backend + Frontend)
- 🔄 **Banco de dados** SQLite → PostgreSQL
- 🔄 **API** Quart → FastAPI
- 🔄 **Frontend** Python → Next.js
- 🔄 **Tipagem** estática com TypeScript
- 🔄 **Documentação** automática da API

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   - Verifique se o PostgreSQL está rodando
   - Confirme as credenciais no .env

2. **Erro de CORS**
   - Verifique se o frontend está na lista de origens permitidas
   - Confirme as URLs no arquivo de configuração

3. **Erro de cache**
   - Limpe o cache: `POST /api/v1/cache/clear`
   - Verifique as estatísticas: `GET /api/v1/cache/stats`

## 📝 Próximos Passos

- [ ] Implementar autenticação de usuários
- [ ] Adicionar testes automatizados
- [ ] Implementar métricas de performance
- [ ] Adicionar notificações em tempo real
- [ ] Implementar exportação de relatórios

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido com ❤️ para facilitar o cálculo de rotas no Brasil**
