-- Script de inicialização do banco de dados PostgreSQL
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configurar timezone
SET timezone = 'America/Sao_Paulo';

-- Criar usuário específico para a aplicação (opcional)
-- CREATE USER routecalc_user WITH PASSWORD 'routecalc_password';
-- GRANT ALL PRIVILEGES ON DATABASE rotas_db TO routecalc_user;

-- Comentário de sucesso
DO $$
BEGIN
    RAISE NOTICE 'Banco de dados inicializado com sucesso!';
END $$;
