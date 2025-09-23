#!/usr/bin/env python3
"""
Script para criar a tabela de erros de upload no banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.upload_error import UploadError

def create_upload_errors_table():
    """Cria a tabela de erros de upload"""
    try:
        print("🔄 Criando tabela upload_errors...")
        
        # Criar a tabela
        UploadError.__table__.create(engine, checkfirst=True)
        
        print("✅ Tabela upload_errors criada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela upload_errors: {str(e)}")
        raise

if __name__ == "__main__":
    create_upload_errors_table()
