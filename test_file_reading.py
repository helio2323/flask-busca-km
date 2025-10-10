#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_file_reading():
    print("=== TESTE DE LEITURA DE ARQUIVO ===")
    
    # 1. Criar grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Leitura Arquivo",
        "descricao": "Teste para verificar quantas linhas são lidas"
    }
    grupo_id = None
    try:
        response = requests.post("http://localhost:8000/api/v1/groups", json=grupo_data)
        if response.status_code == 200:
            grupo = response.json()
            grupo_id = grupo['id']
            print(f"[OK] Grupo criado: ID {grupo_id}")
        else:
            print(f"[ERRO] Erro ao criar grupo: {response.status_code}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao criar grupo: {e}")
        return
    
    # 2. Criar arquivo com 8 rotas (mais que 4)
    print(f"\n2. Criando arquivo com 8 rotas...")
    data = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8],
        'Origem': ['CAMPINAS', 'CAMPINAS', 'CAMPINAS', 'CAMPINAS', 'CAMPINAS', 'CAMPINAS', 'CAMPINAS', 'CAMPINAS'],
        'UF': ['Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo'],
        'Destino (Cidade/Estado)': ['ADAMANTINA', 'ADOLFO', 'AGUAI', 'AGUAS DA PRATA', 'AMERICANA', 'AMPARO', 'ARARAS', 'ARTUR NOGUEIRA'],
        'UF.1': ['Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo', 'Sao Paulo'],
        'KM': [0, 0, 0, 0, 0, 0, 0, 0],
        'Pedágio': [0, 0, 0, 0, 0, 0, 0, 0]
    }
    df = pd.DataFrame(data)
    
    print(f"[DEBUG] DataFrame criado com {len(df)} linhas")
    print(f"[DEBUG] Colunas: {df.columns.tolist()}")
    print(f"[DEBUG] Primeiras 3 linhas:")
    print(df.head(3).to_string())
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Rotas')
    output.seek(0)
    print(f"[OK] Arquivo Excel criado com {len(df)} linhas")
    
    # 3. Upload
    print(f"\n3. Fazendo upload para grupo {grupo_id}...")
    upload_id = None
    try:
        files = {'file': ('test_8_routes.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        response = requests.post(f"http://localhost:8000/api/v1/routes/upload?grupo_id={grupo_id}", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            upload_id = upload_result['upload_id']
            total_rotas = upload_result.get('total_rotas', 'N/A')
            print(f"[OK] Upload realizado: ID {upload_id}")
            print(f"[DEBUG] Total de rotas reportado: {total_rotas}")
            print(f"[DEBUG] Grupo ID passado: {grupo_id}")
            print(f"[DEBUG] Upload ID gerado: {upload_id}")
        else:
            print(f"[ERRO] Erro no upload: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"[ERRO] Erro no upload: {e}")
        return
    
    # 4. Monitorar processamento
    print(f"\n4. Monitorando processamento...")
    max_tentativas = 20
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
        time.sleep(3)
    
    # 5. Verificar grupo
    print(f"\n5. Verificando grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Grupo encontrado:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Distancia total: {grupo_data.get('total_distancia', 'N/A')} km")
            print(f"  Pedagios totais: R$ {grupo_data.get('total_pedagios', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")
    
    # 6. Verificar rotas do grupo
    print(f"\n6. Verificando rotas do grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            
            if rotas:
                print("\nRotas encontradas:")
                for i, rota in enumerate(rotas, 1):
                    print(f"  {i}. {rota.get('origem', 'N/A')} -> {rota.get('destino', 'N/A')}")
                    print(f"     Distancia: {rota.get('distancia', 'N/A')} km")
                    print(f"     Pedagios: R$ {rota.get('pedagios', 'N/A')}")
                    print(f"     Data: {rota.get('data_consulta', 'N/A')}")
                    print()
            else:
                print("Nenhuma rota encontrada no grupo")
        else:
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")
    
    print(f"\n=== DIAGNÓSTICO ===")
    print(f"Se apenas 4 rotas foram processadas de 8 enviadas,")
    print(f"então há um problema na leitura do arquivo ou no processamento.")

if __name__ == "__main__":
    test_file_reading()
