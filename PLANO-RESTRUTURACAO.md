# Plano de Reestruturação - Sistema de Cálculo de Rotas

## Análise do Estado Atual

### Backend Atual (Python/Quart)
- **Arquivo principal**: `index.py` (658 linhas)
- **Funcionalidades principais**:
  - Cálculo de rotas individuais e múltiplas
  - Integração com API rotasbrasil.com.br
  - Sistema de cache (coordenadas, rotas, sugestões)
  - Upload e processamento de planilhas Excel
  - Histórico de consultas (SQLite)
  - Geocodificação com Nominatim
  - Cálculo de pedágios

### Frontend Atual (Next.js/React)
- **Localização**: `route-frontend/`
- **Tecnologias**: Next.js 14, React 18, TypeScript, Tailwind CSS, Radix UI
- **Componentes principais**:
  - `RouteCalculator`: Calculadora de rotas individuais
  - `FileUpload`: Upload de planilhas Excel
  - `RouteHistory`: Histórico de rotas
  - `Dashboard`: Painel principal
  - `GroupManager`: Gerenciamento de grupos

## Objetivos da Reestruturação

1. **Separar responsabilidades**: Backend puro (API) + Frontend (Next.js)
2. **Migrar banco de dados**: SQLite → PostgreSQL
3. **Criar API RESTful** para comunicação frontend-backend
4. **Manter funcionalidades core** de cálculo de rotas
5. **Melhorar arquitetura** e manutenibilidade

## Plano de Execução

### FASE 1: Análise e Preparação (1-2 horas)
- [x] Analisar código atual e funcionalidades
- [x] Identificar dependências e integrações
- [x] Mapear endpoints necessários para o frontend
- [x] Definir estrutura do banco PostgreSQL

### FASE 2: Configuração do Ambiente (1 hora)
- [ ] Configurar PostgreSQL localmente
- [ ] Criar estrutura de pastas para o novo backend
- [ ] Configurar Docker Compose para desenvolvimento
- [ ] Instalar dependências Python necessárias

### FASE 3: Criação do Banco de Dados (1 hora)
- [ ] Criar schema PostgreSQL
- [ ] Migrar dados do SQLite (se necessário)
- [ ] Configurar conexão com banco
- [ ] Criar modelos SQLAlchemy

### FASE 4: Desenvolvimento da API (3-4 horas)
- [ ] Criar estrutura base da API (FastAPI)
- [ ] Implementar endpoints de cálculo de rotas
- [ ] Implementar sistema de cache
- [ ] Implementar upload de arquivos
- [ ] Implementar histórico de consultas
- [ ] Implementar sugestões de cidades

### FASE 5: Integração Frontend-Backend (2-3 horas)
- [ ] Configurar variáveis de ambiente
- [ ] Atualizar componentes para consumir API
- [ ] Implementar tratamento de erros
- [ ] Testar integração completa

### FASE 6: Limpeza e Otimização (1 hora)
- [ ] Remover arquivos antigos do frontend Python
- [ ] Atualizar documentação
- [ ] Configurar scripts de desenvolvimento
- [ ] Testes finais

## Estrutura Proposta

```
flask-busca-km/
├── backend/                    # Novo backend API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # Endpoints
│   │   ├── core/              # Configurações
│   │   ├── services/          # Lógica de negócio
│   │   └── utils/             # Utilitários
│   ├── requirements.txt
│   └── Dockerfile
├── route-frontend/            # Frontend Next.js (manter)
├── docker-compose.yml         # Para desenvolvimento
├── .env.example
└── README.md
```

## Endpoints da API Necessários

### Rotas
- `POST /api/routes/calculate` - Calcular rota individual
- `POST /api/routes/calculate-multiple` - Calcular rota múltipla
- `POST /api/routes/upload` - Upload de planilha Excel
- `GET /api/routes/history` - Histórico de rotas
- `DELETE /api/routes/history/{id}` - Deletar rota do histórico

### Sugestões
- `GET /api/suggestions/{term}` - Sugestões de cidades

### Cache
- `GET /api/cache/stats` - Estatísticas do cache
- `POST /api/cache/clear` - Limpar cache

### Grupos
- `GET /api/groups` - Listar grupos
- `POST /api/groups` - Criar grupo
- `PUT /api/groups/{id}` - Atualizar grupo
- `DELETE /api/groups/{id}` - Deletar grupo

## Banco de Dados PostgreSQL

### Tabelas Principais

```sql
-- Consultas de rotas
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

-- Grupos de rotas
CREATE TABLE grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cache de coordenadas
CREATE TABLE cache_coordenadas (
    id SERIAL PRIMARY KEY,
    cidade VARCHAR(255) UNIQUE NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TIMESTAMP NOT NULL
);

-- Cache de rotas
CREATE TABLE cache_rotas (
    id SERIAL PRIMARY KEY,
    chave_rota VARCHAR(255) UNIQUE NOT NULL,
    resultado JSONB NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TIMESTAMP NOT NULL
);
```

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Alembic**: Migrações de banco
- **Pydantic**: Validação de dados
- **Redis**: Cache (opcional, para produção)
- **Celery**: Processamento assíncrono (opcional)

### Frontend (manter)
- **Next.js 14**: Framework React
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização
- **Radix UI**: Componentes acessíveis

### Infraestrutura
- **PostgreSQL**: Banco de dados principal
- **Docker**: Containerização
- **Docker Compose**: Orquestração local

## Considerações Importantes

1. **Manter compatibilidade**: Preservar funcionalidades existentes
2. **Performance**: Manter sistema de cache eficiente
3. **Escalabilidade**: Estrutura preparada para crescimento
4. **Manutenibilidade**: Código limpo e bem documentado
5. **Testes**: Implementar testes unitários e de integração

## Próximos Passos

1. Confirmar aprovação do plano
2. Iniciar FASE 2: Configuração do ambiente
3. Executar fases sequencialmente
4. Testes e validação final

---

**Tempo estimado total**: 8-12 horas
**Riscos identificados**: Migração de dados, compatibilidade de APIs externas
**Mitigações**: Backup completo, testes incrementais, rollback plan
