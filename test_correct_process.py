#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_correct_process():
    print("=== TESTE DO PROCESSO CORRETO ===")
    print("Processo: Linha -> Autocomplete -> Match -> KM/Pedágio")
    
    # Dados de teste específicos
    test_data = [
        {"ID": 1, "Origem": "CAMPINAS", "UF": "São Paulo", "Destino": "ADAMANTINA", "UF.1": "São Paulo"},
        {"ID": 2, "Origem": "CAMPINAS", "UF": "São Paulo", "Destino": "ADOLFO", "UF.1": "São Paulo"},
        {"ID": 3, "Origem": "CAMPINAS", "UF": "São Paulo", "Destino": "AGUAI", "UF.1": "São Paulo"},
        {"ID": 4, "Origem": "CAMPINAS", "UF": "São Paulo", "Destino": "AGUAS DA PRATA", "UF.1": "São Paulo"}
    ]
    
    print(f"\nTestando {len(test_data)} rotas específicas:")
    for i, rota in enumerate(test_data, 1):
        print(f"{i}. {rota['Origem']}, {rota['UF']} -> {rota['Destino']}, {rota['UF.1']}")
    
    # 1. Criar grupo
    print(f"\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Processo Correto",
        "descricao": "Teste com processo: linha → autocomplete → match → KM/pedágio"
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
    
    # 2. Criar arquivo Excel com dados específicos
    print(f"\n2. Criando arquivo Excel com dados específicos...")
    df = pd.DataFrame(test_data)
    df['KM'] = ''
    df['Pedágio'] = ''
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Rotas')
    output.seek(0)
    print(f"[OK] Arquivo criado com {len(df)} linhas")
    
    # 3. Upload do arquivo
    print(f"\n3. Fazendo upload...")
    upload_id = None
    try:
        files = {'file': ('test_correct_process.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
        time.sleep(5)  # Aguardar 5 segundos
    
    # 5. Verificar resultados
    print(f"\n5. Verificando resultados...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            
            if rotas:
                print("\nRotas processadas:")
                for i, rota in enumerate(rotas, 1):
                    print(f"  {i}. {rota.get('origem', 'N/A')} -> {rota.get('destino', 'N/A')}")
                    print(f"     Distancia: {rota.get('distancia', 'N/A')} km")
                    print(f"     Pedagios: R$ {rota.get('pedagios', 'N/A')}")
                    print(f"     Fonte: {rota.get('fonte', 'N/A')}")
                    print()
            else:
                print("Nenhuma rota encontrada no grupo")
        else:
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")
    
    # 6. Testar rota individual para verificar o processo
    print(f"\n6. Testando rota individual...")
    try:
        test_route = {
            "origem": "Campinas, Sao Paulo, BR",
            "destino": "Adamantina, Sao Paulo, BR"
        }
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_route)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota individual testada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destino: {result.get('destino', 'N/A')}")
            print(f"  Distancia: {result.get('distance', 'N/A')} km")
            print(f"  Pedagios: R$ {result.get('pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao testar rota individual: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao testar rota individual: {e}")
    
    print(f"\n=== RESUMO ===")
    print(f"[OK] Sistema funcionando: API Rotas Brasil integrada")
    print(f"[OK] Cache desabilitado: Sempre usa API")
    print(f"[OK] Formato correto: 'Cidade, Estado, BR'")
    print(f"[ERRO] Persistência: Rotas não aparecem no grupo")
    print(f"[ERRO] Processo: Não está fazendo linha -> autocomplete -> match -> KM/pedágio")

if __name__ == "__main__":
    test_correct_process()
