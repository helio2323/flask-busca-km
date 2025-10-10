#!/usr/bin/env python3
import requests
import pandas as pd
import time

def test_new_upload():
    print("=== TESTE NOVO UPLOAD ===")
    
    # 1. Criar novo grupo
    print("\n1. Criando novo grupo...")
    grupo_data = {
        "nome": "Teste Novo Upload",
        "descricao": "Teste com arquivo rotas.xlsx - segunda tentativa"
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
    
    # 2. Fazer upload apenas das 2 primeiras rotas (que sabemos que funcionam)
    print("\n2. Criando arquivo de teste com 2 rotas...")
    try:
        df = pd.read_excel("rotas.xlsx")
        df_teste = df.head(2)  # Apenas as 2 primeiras linhas
        
        # Salvar arquivo de teste
        df_teste.to_excel("rotas_teste_2.xlsx", index=False)
        print(f"[OK] Arquivo de teste criado com {len(df_teste)} rotas")
        
        # Fazer upload
        with open("rotas_teste_2.xlsx", "rb") as f:
            files = {'file': ('rotas_teste_2.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
    
    # 3. Monitorar processamento
    print(f"\n3. Monitorando processamento...")
    max_tentativas = 10
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
            if response.status_code == 200:
                status = response.json()
                print(f"Status: {status['status']} - Processadas: {status.get('rotas_processadas', 0)}/{status.get('total_rotas', 0)} - Erros: {status.get('rotas_com_erro', 0)}")
                
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
        time.sleep(5)  # Aguardar 5 segundos
    
    # 4. Verificar resultados
    print(f"\n4. Verificando resultados...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            
            for i, rota in enumerate(rotas):
                print(f"\nRota {i+1}:")
                print(f"  Origem: {rota.get('origem', 'N/A')}")
                print(f"  Destino: {rota.get('destino', 'N/A')}")
                print(f"  Distância: {rota.get('distancia', 'N/A')} km")
                print(f"  Pedágios: R$ {rota.get('pedagios', 'N/A')}")
                print(f"  Fonte: {rota.get('fonte', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")

if __name__ == "__main__":
    test_new_upload()
