#!/usr/bin/env python3
"""
Script para inicializar o banco de dados PostgreSQL
"""
import asyncio
from sqlalchemy import create_engine
from app.core.database import Base
from app.core.config import settings

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    try:
        # Criar engine
        engine = create_engine(settings.database_url)
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Banco de dados inicializado com sucesso!")
        print(f"📊 Tabelas criadas:")
        print("   - consultas")
        print("   - grupos") 
        print("   - cache_coordenadas")
        print("   - cache_rotas")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return False
    
    return True

if __name__ == "__main__":
    init_database()
