#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_database_save():
    print("=== TESTE DE SALVAMENTO NO BANCO ===")
    
    # 1. Criar grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Salvamento",
        "descricao": "Teste para verificar se consultas são salvas no banco"
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
    
    # 2. Criar arquivo com 1 rota apenas
    print(f"\n2. Criando arquivo com 1 rota...")
    data = {
        'ID': [1],
        'Origem': ['CAMPINAS'],
        'UF': ['Sao Paulo'],
        'Destino (Cidade/Estado)': ['ADAMANTINA'],
        'UF.1': ['Sao Paulo'],
        'KM': [0],
        'Pedágio': [0]
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Rotas')
    output.seek(0)
    print(f"[OK] Arquivo criado com 1 rota")
    
    # 3. Upload
    print(f"\n3. Fazendo upload...")
    upload_id = None
    try:
        files = {'file': ('test_save.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
    max_tentativas = 10
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
    
    # 5. Verificar estatísticas gerais
    print(f"\n5. Verificando estatísticas gerais...")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] Estatísticas gerais:")
            print(f"  Total de grupos: {stats.get('total_grupos', 'N/A')}")
            print(f"  Total de rotas: {stats.get('total_rotas', 'N/A')}")
            print(f"  Distancia total: {stats.get('total_distancia', 'N/A')} km")
            print(f"  Pedagios totais: R$ {stats.get('total_pedagios', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar estatísticas: {e}")
    
    # 6. Verificar grupo específico
    print(f"\n6. Verificando grupo {grupo_id}...")
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
    
    # 7. Verificar rotas do grupo
    print(f"\n7. Verificando rotas do grupo {grupo_id}...")
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
    print(f"Se as estatísticas gerais mostram rotas mas o grupo não tem rotas,")
    print(f"então o problema está na associação grupo_id das consultas.")

if __name__ == "__main__":
    test_database_save()
