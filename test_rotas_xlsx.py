#!/usr/bin/env python3
import requests
import pandas as pd
import time
import json

def test_rotas_xlsx():
    """Testa o upload do arquivo rotas.xlsx"""
    
    print("=== TESTE COM ARQUIVO rotas.xlsx ===")
    
    # 1. Primeiro, criar um grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste rotas.xlsx",
        "descricao": "Teste com arquivo real rotas.xlsx"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/groups", json=grupo_data)
        if response.status_code == 200:
            grupo = response.json()
            grupo_id = grupo['id']
            print(f"[OK] Grupo criado: ID {grupo_id}")
        else:
            print(f"[ERRO] Erro ao criar grupo: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao criar grupo: {e}")
        return
    
    # 2. Ler o arquivo rotas.xlsx para verificar conteúdo
    print("\n2. Verificando conteúdo do arquivo rotas.xlsx...")
    try:
        df = pd.read_excel("rotas.xlsx")
        print(f"[OK] Arquivo lido: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        print("\nPrimeiras 3 linhas:")
        print(df.head(3).to_string())
    except Exception as e:
        print(f"[ERRO] Erro ao ler arquivo: {e}")
        return
    
    # 3. Fazer upload do arquivo
    print(f"\n3. Fazendo upload do arquivo para grupo {grupo_id}...")
    try:
        with open("rotas.xlsx", "rb") as f:
            files = {'file': ('rotas.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(f"http://localhost:8000/api/v1/routes/upload?grupo_id={grupo_id}", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            upload_id = upload_result['upload_id']
            print(f"[OK] Upload realizado: ID {upload_id}")
        else:
            print(f"[ERRO] Erro no upload: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"[ERRO] Erro no upload: {e}")
        return
    
    # 4. Monitorar processamento
    print(f"\n4. Monitorando processamento...")
    max_tentativas = 30  # 5 minutos máximo
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
            if response.status_code == 200:
                status = response.json()
                print(f"Status: {status['status']} - Processadas: {status['processadas']}/{status['total']} - Erros: {status['erros']}")
                
                if status['status'] == 'completed':
                    print("[OK] Processamento concluído!")
                    break
                elif status['status'] == 'error':
                    print("[ERRO] Erro no processamento!")
                    break
            else:
                print(f"[ERRO] Erro ao verificar status: {response.status_code}")
                break
        except Exception as e:
            print(f"[ERRO] Erro ao verificar status: {e}")
            break
        
        tentativa += 1
        time.sleep(10)  # Aguardar 10 segundos
    
    # 5. Verificar rotas processadas
    print(f"\n5. Verificando rotas processadas...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            rotas = response.json()
            print(f"[OK] {len(rotas)} rotas encontradas")
            
            if rotas:
                print("\nPrimeiras 3 rotas:")
                for i, rota in enumerate(rotas[:3]):
                    print(f"Rota {i+1}:")
                    print(f"  Origem: {rota.get('origem', 'N/A')}")
                    print(f"  Destino: {rota.get('destino', 'N/A')}")
                    print(f"  Distância: {rota.get('distancia', 'N/A')} km")
                    print(f"  Pedágios: R$ {rota.get('pedagios', 'N/A')}")
                    print(f"  Fonte: {rota.get('fonte', 'N/A')}")
                    print()
        else:
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")
    
    # 6. Verificar estatísticas do grupo
    print(f"\n6. Verificando estatísticas do grupo...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            print(f"[OK] Estatísticas do grupo:")
            print(f"  Total de rotas: {grupo_info.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {grupo_info.get('distancia_total', 'N/A')} km")
            print(f"  Pedágios totais: R$ {grupo_info.get('pedagios_total', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")

if __name__ == "__main__":
    test_rotas_xlsx()
