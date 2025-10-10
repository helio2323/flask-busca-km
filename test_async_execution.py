#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_async_execution():
    print("=== TESTE DE EXECUÇÃO ASSÍNCRONA ===")
    
    # 1. Criar grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Async",
        "descricao": "Teste para verificar execução assíncrona"
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
    print(f"\n3. Fazendo upload para grupo {grupo_id}...")
    upload_id = None
    try:
        files = {'file': ('test_async.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        response = requests.post(f"http://localhost:8000/api/v1/routes/upload?grupo_id={grupo_id}", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            upload_id = upload_result['upload_id']
            print(f"[OK] Upload realizado: ID {upload_id}")
            print(f"[DEBUG] Grupo ID passado: {grupo_id}")
            print(f"[DEBUG] Upload ID gerado: {upload_id}")
        else:
            print(f"[ERRO] Erro no upload: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"[ERRO] Erro no upload: {e}")
        return
    
    # 4. Verificar status imediatamente
    print(f"\n4. Verificando status imediatamente...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
        if response.status_code == 200:
            status = response.json()
            print(f"Status imediato: {status['status']} - Processadas: {status['rotas_processadas']}/{status['total_rotas']} - Erros: {status['rotas_com_erro']}")
        else:
            print(f"[ERRO] Erro ao verificar status: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao verificar status: {e}")
    
    # 5. Aguardar e verificar novamente
    print(f"\n5. Aguardando 5 segundos e verificando novamente...")
    time.sleep(5)
    
    try:
        response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
        if response.status_code == 200:
            status = response.json()
            print(f"Status após 5s: {status['status']} - Processadas: {status['rotas_processadas']}/{status['total_rotas']} - Erros: {status['rotas_com_erro']}")
        else:
            print(f"[ERRO] Erro ao verificar status: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao verificar status: {e}")
    
    # 6. Verificar grupo
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
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se o status muda para 'completed' mas não vemos logs,")
    print(f"então há um problema na execução assíncrona do FastAPI.")

if __name__ == "__main__":
    test_async_execution()
