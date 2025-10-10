#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_fixed_system():
    print("=== TESTE DO SISTEMA CORRIGIDO ===")

    # 1. Criar um novo grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Sistema Corrigido",
        "descricao": "Teste após correção da validação"
    }
    grupo_id = None
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

    # 2. Criar um arquivo Excel de teste com 2 rotas que sabemos que funcionam
    print("\n2. Criando arquivo de teste...")
    data = {
        'ID': [1, 2],
        'Origem': ['CAMPINAS', 'CAMPINAS'],
        'UF': ['Sao Paulo', 'Sao Paulo'],
        'Destino (Cidade/Estado)': ['ADAMANTINA', 'ADOLFO'],
        'UF.1': ['Sao Paulo', 'Sao Paulo'],
        'KM': [0, 0],
        'Pedágio': [0, 0]
    }
    df_test = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_test.to_excel(writer, index=False, sheet_name='Rotas')
    output.seek(0)
    print("[OK] Arquivo de teste criado com 2 rotas")

    # 3. Fazer upload do arquivo
    print(f"\n3. Fazendo upload do arquivo para grupo {grupo_id}...")
    upload_id = None
    try:
        files = {'file': ('test_fixed.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
    max_tentativas = 30
    tentativa = 0
    while tentativa < max_tentativas:
        try:
            response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
            if response.status_code == 200:
                status = response.json()
                print(f"Status: {status['status']} - Processadas: {status['rotas_processadas']}/{status['total_rotas']} - Erros: {status['rotas_com_erro']}")
                
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
        time.sleep(10)

    # 5. Verificar rotas processadas no grupo
    print("\n5. Verificando resultados...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            if rotas:
                for i, rota in enumerate(rotas):
                    print(f"  Rota {i+1}: {rota.get('origem')} -> {rota.get('destino')} ({rota.get('distancia')} km, R$ {rota.get('pedagios')})")
        else:
            print(f"[ERRO] Erro ao buscar rotas do grupo: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas do grupo: {e}")

    # 6. Verificar estatísticas do grupo
    print(f"\n6. Verificando estatísticas do grupo...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Estatísticas do grupo:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {grupo_data.get('total_distancia', 'N/A')} km")
            print(f"  Pedágios totais: R$ {grupo_data.get('total_pedagios', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar estatísticas do grupo: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar estatísticas do grupo: {e}")

if __name__ == "__main__":
    test_fixed_system()
