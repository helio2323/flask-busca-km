#!/usr/bin/env python3
import pandas as pd
import os

def check_real_file():
    print("=== VERIFICAÇÃO DO ARQUIVO REAL ===")
    
    # Verificar se existe o arquivo rotas.xlsx
    file_path = "rotas.xlsx"
    
    if not os.path.exists(file_path):
        print(f"[ERRO] Arquivo {file_path} não encontrado!")
        print("Arquivos Excel encontrados no diretório:")
        for file in os.listdir("."):
            if file.endswith(('.xlsx', '.xls')):
                print(f"  - {file}")
        return
    
    print(f"[OK] Arquivo {file_path} encontrado!")
    
    try:
        # Ler o arquivo
        df = pd.read_excel(file_path)
        
        print(f"\n[INFO] Arquivo lido com sucesso:")
        print(f"  Total de linhas: {len(df)}")
        print(f"  Total de colunas: {len(df.columns)}")
        print(f"  Colunas encontradas: {df.columns.tolist()}")
        
        # Mostrar primeiras linhas
        print(f"\n[INFO] Primeiras 5 linhas:")
        print(df.head().to_string())
        
        # Verificar se há linhas vazias
        linhas_vazias = df.isnull().all(axis=1).sum()
        print(f"\n[INFO] Linhas completamente vazias: {linhas_vazias}")
        
        # Verificar colunas importantes
        colunas_origem = [col for col in df.columns if 'origem' in col.lower()]
        colunas_destino = [col for col in df.columns if 'destino' in col.lower()]
        
        print(f"\n[INFO] Colunas de origem encontradas: {colunas_origem}")
        print(f"[INFO] Colunas de destino encontradas: {colunas_destino}")
        
        # Verificar dados não nulos
        if colunas_origem:
            origem_nao_nula = df[colunas_origem[0]].notna().sum()
            print(f"[INFO] Linhas com origem não nula: {origem_nao_nula}")
        
        if colunas_destino:
            destino_nao_nula = df[colunas_destino[0]].notna().sum()
            print(f"[INFO] Linhas com destino não nula: {destino_nao_nula}")
        
        # Mostrar estatísticas por coluna
        print(f"\n[INFO] Estatísticas por coluna:")
        for col in df.columns:
            nao_nulos = df[col].notna().sum()
            print(f"  {col}: {nao_nulos} valores não nulos")
        
    except Exception as e:
        print(f"[ERRO] Erro ao ler arquivo: {e}")

if __name__ == "__main__":
    check_real_file()
