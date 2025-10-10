#!/usr/bin/env python3
"""
Script para adicionar colunas UF ao banco de dados
"""
import sqlite3
import os

def migrate_database():
    print("=== MIGRAÇÃO DO BANCO DE DADOS ===")
    
    # Caminho do banco de dados
    db_path = "backend/rotas.db"
    
    if not os.path.exists(db_path):
        print(f"[ERRO] Banco de dados não encontrado: {db_path}")
        return
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"[OK] Conectado ao banco: {db_path}")
        
        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(consultas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"[INFO] Colunas existentes: {columns}")
        
        # Adicionar coluna uf_origem se não existir
        if 'uf_origem' not in columns:
            print("[INFO] Adicionando coluna uf_origem...")
            cursor.execute("ALTER TABLE consultas ADD COLUMN uf_origem VARCHAR(10)")
            print("[OK] Coluna uf_origem adicionada")
        else:
            print("[OK] Coluna uf_origem já existe")
        
        # Adicionar coluna uf_destino se não existir
        if 'uf_destino' not in columns:
            print("[INFO] Adicionando coluna uf_destino...")
            cursor.execute("ALTER TABLE consultas ADD COLUMN uf_destino VARCHAR(10)")
            print("[OK] Coluna uf_destino adicionada")
        else:
            print("[OK] Coluna uf_destino já existe")
        
        # Verificar as colunas após a migração
        cursor.execute("PRAGMA table_info(consultas)")
        columns_after = [column[1] for column in cursor.fetchall()]
        print(f"[INFO] Colunas após migração: {columns_after}")
        
        # Commit das mudanças
        conn.commit()
        print("[OK] Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Erro na migração: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
