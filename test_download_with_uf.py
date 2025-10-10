#!/usr/bin/env python3
import requests
import pandas as pd
import io
import time

def test_download_with_uf():
    print("=== TESTE DE DOWNLOAD COM COLUNAS UF ===")
    
    # 1. Criar grupo
    print("\n1. Criando grupo...")
    grupo_data = {
        "nome": "Teste Download UF",
        "descricao": "Teste para verificar se UF aparece no download"
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
    
    # 2. Criar arquivo com 3 rotas
    print(f"\n2. Criando arquivo com 3 rotas...")
    data = {
        'ID': [1, 2, 3],
        'Origem': ['CAMPINAS', 'CAMPINAS', 'CAMPINAS'],
        'UF': ['Sao Paulo', 'Sao Paulo', 'Sao Paulo'],
        'Destino (Cidade/Estado)': ['ADAMANTINA', 'ADOLFO', 'AGUAI'],
        'UF.1': ['Sao Paulo', 'Sao Paulo', 'Sao Paulo'],
        'KM': [0, 0, 0],
        'Pedágio': [0, 0, 0]
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Rotas')
    output.seek(0)
    print(f"[OK] Arquivo criado com {len(df)} rotas")
    
    # 3. Upload
    print(f"\n3. Fazendo upload para grupo {grupo_id}...")
    upload_id = None
    try:
        files = {'file': ('test_uf_download.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
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
    max_tentativas = 15
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
    
    # 5. Testar download
    print(f"\n5. Testando download do grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/download")
        if response.status_code == 200:
            print(f"[OK] Download realizado com sucesso!")
            print(f"[INFO] Tamanho do arquivo: {len(response.content)} bytes")
            
            # Salvar arquivo para verificação
            with open("test_download_uf.xlsx", "wb") as f:
                f.write(response.content)
            print(f"[OK] Arquivo salvo como test_download_uf.xlsx")
            
            # Verificar conteúdo do arquivo baixado
            df_download = pd.read_excel("test_download_uf.xlsx")
            print(f"\n[INFO] Arquivo baixado:")
            print(f"  Total de linhas: {len(df_download)}")
            print(f"  Colunas: {df_download.columns.tolist()}")
            print(f"\n[INFO] Primeiras 3 linhas:")
            print(df_download.head(3).to_string())
            
            # Verificar se as colunas UF estão presentes
            if 'UF' in df_download.columns and 'UF.1' in df_download.columns:
                print(f"\n[OK] Colunas UF encontradas no download!")
                print(f"  UF (origem): {df_download['UF'].tolist()}")
                print(f"  UF.1 (destino): {df_download['UF.1'].tolist()}")
            else:
                print(f"\n[ERRO] Colunas UF não encontradas no download!")
                print(f"  Colunas disponíveis: {df_download.columns.tolist()}")
        else:
            print(f"[ERRO] Erro no download: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro no download: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se as colunas UF aparecem no download, então a correção funcionou!")

if __name__ == "__main__":
    test_download_with_uf()
