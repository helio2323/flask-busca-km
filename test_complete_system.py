#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_complete_system():
    print("=== TESTE COMPLETO DO SISTEMA ===")

    # 1. Criar um novo grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Sistema Completo",
        "descricao": "Teste com arquivo rotas.xlsx usando novo formato"
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

    # 2. Ler o arquivo rotas.xlsx para verificar conteúdo
    print("\n2. Verificando conteúdo do arquivo rotas.xlsx...")
    try:
        df = pd.read_excel("rotas.xlsx")
        print(f"[OK] Arquivo lido: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        print("\nPrimeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Verificar se tem as colunas necessárias
        has_uf = 'UF' in df.columns and 'UF.1' in df.columns
        print(f"\nTem colunas UF: {has_uf}")
        if has_uf:
            print("Formato detectado: NOVO (com UF)")
        else:
            print("Formato detectado: ANTIGO (sem UF)")
            
    except Exception as e:
        print(f"[ERRO] Erro ao ler arquivo: {e}")
        return

    # 3. Fazer upload do arquivo
    print(f"\n3. Fazendo upload do arquivo para grupo {grupo_id}...")
    upload_id = None
    try:
        with open("rotas.xlsx", "rb") as f:
            files = {'file': ('rotas.xlsx', f.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
        time.sleep(10)  # Aguardar 10 segundos

    # 5. Verificar rotas processadas
    print(f"\n5. Verificando rotas processadas...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
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
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Estatísticas do grupo:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {grupo_data.get('total_distancia', 'N/A')} km")
            print(f"  Pedágios totais: R$ {grupo_data.get('total_pedagios', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")

    # 7. Testar uma rota individual para verificar formato
    print(f"\n7. Testando rota individual...")
    try:
        test_data = {
            "origem": "Campinas, Sao Paulo, BR",
            "destino": "Adamantina, Sao Paulo, BR"
        }
        response = requests.post("http://localhost:8000/api/v1/routes/process-individual", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota individual calculada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destino: {result.get('destino', 'N/A')}")
            print(f"  Distância: {result.get('distance', 'N/A')} km")
            print(f"  Pedágios: R$ {result.get('pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao calcular rota individual: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao calcular rota individual: {e}")

if __name__ == "__main__":
    test_complete_system()
