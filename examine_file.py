#!/usr/bin/env python3
import pandas as pd

def examine_file():
    print("=== EXAMINANDO ARQUIVO rotas.xlsx ===")
    
    try:
        df = pd.read_excel("rotas.xlsx")
        print(f"Arquivo lido com sucesso: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        
        print("\nConteúdo completo:")
        print(df.to_string())
        
        print("\nTipos de dados:")
        print(df.dtypes)
        
        print("\nValores nulos:")
        print(df.isnull().sum())
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

if __name__ == "__main__":
    examine_file()
