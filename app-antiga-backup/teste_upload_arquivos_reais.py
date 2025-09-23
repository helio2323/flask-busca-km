import requests
import pandas as pd
import io
import time
import os

def testar_upload_arquivo(caminho_arquivo, nome_arquivo, grupo_id=3):
    """Testa o upload de um arquivo Excel para um grupo"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTANDO UPLOAD: {nome_arquivo}")
    print(f"{'='*60}")
    
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(caminho_arquivo)
        print(f"📊 Arquivo lido com sucesso!")
        print(f"📋 Colunas encontradas: {list(df.columns)}")
        print(f"📈 Total de linhas: {len(df)}")
        
        # Verificar se tem as colunas necessárias
        required_columns = ['origem', 'destino']
        if not all(col in df.columns for col in required_columns):
            print(f"❌ ERRO: Arquivo não contém as colunas necessárias: {required_columns}")
            print(f"📋 Colunas disponíveis: {list(df.columns)}")
            return False
        
        # Mostrar algumas linhas de exemplo
        print(f"\n📋 Primeiras 5 linhas do arquivo:")
        print(df.head().to_string())
        
        # Salvar em Excel em memória para upload
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Rotas', index=False)
        output.seek(0)
        
        # Fazer upload
        url = "http://localhost:8000/api/v1/routes/upload"
        files = {'file': (nome_arquivo, output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        params = {'grupo_id': grupo_id}
        
        print(f"\n🚀 Fazendo upload para o grupo {grupo_id}...")
        response = requests.post(url, files=files, params=params)
        
        if response.status_code == 200:
            print("✅ Upload realizado com sucesso!")
            upload_data = response.json()
            print(f"📊 Resposta: {upload_data}")
            
            # Aguardar processamento
            upload_id = upload_data.get('upload_id')
            if upload_id:
                print(f"\n⏳ Aguardando processamento (ID: {upload_id})...")
                awaitar_processamento(upload_id)
            
            return True
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"📝 Detalhes: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        return False

def awaitar_processamento(upload_id, max_tentativas=60):
    """Aguarda o processamento do upload"""
    for tentativa in range(max_tentativas):
        try:
            response = requests.get(f"http://localhost:8000/api/v1/routes/upload-status/{upload_id}")
            if response.status_code == 200:
                status = response.json()
                print(f"📊 Status: {status['status']} - Progresso: {status.get('progresso', 0)}%")
                
                if status['status'] == 'completed':
                    print("✅ Processamento concluído!")
                    print(f"📈 Rotas processadas: {status.get('rotas_processadas', 0)}")
                    print(f"❌ Rotas com erro: {status.get('rotas_com_erro', 0)}")
                    break
                elif status['status'] == 'error':
                    print(f"❌ Erro no processamento: {status.get('erro', 'Erro desconhecido')}")
                    break
            else:
                print(f"⚠️ Erro ao verificar status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Erro ao verificar status: {str(e)}")
        
        time.sleep(2)  # Aguardar 2 segundos antes da próxima verificação

def verificar_grupo(grupo_id):
    """Verifica as estatísticas do grupo após upload"""
    print(f"\n🔍 Verificando estatísticas do grupo {grupo_id}...")
    
    try:
        # Verificar estatísticas do grupo
        grupo_response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if grupo_response.status_code == 200:
            grupo = grupo_response.json()
            print(f"📊 Grupo: {grupo['nome']}")
            print(f"📈 Total de rotas: {grupo['total_rotas']}")
            print(f"🛣️ Total de distância: {grupo['total_distancia']} km")
            print(f"💰 Total de pedágios: R$ {grupo['total_pedagios']}")
        else:
            print(f"❌ Erro ao buscar grupo: {grupo_response.status_code}")
            return False
        
        # Verificar rotas do grupo
        print(f"\n🔍 Verificando rotas do grupo...")
        rotas_response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if rotas_response.status_code == 200:
            rotas = rotas_response.json()
            print(f"📊 Total de rotas no grupo: {rotas['total_rotas']}")
            
            # Mostrar algumas rotas de exemplo
            if rotas['rotas']:
                print(f"\n📋 Primeiras 5 rotas:")
                for i, rota in enumerate(rotas['rotas'][:5], 1):
                    print(f"  {i}. {rota['origem']} → {rota['destino']} ({rota['distancia']} km, R$ {rota['pedagios']})")
                
                if len(rotas['rotas']) > 5:
                    print(f"  ... e mais {len(rotas['rotas']) - 5} rotas")
            else:
                print("⚠️ Nenhuma rota encontrada no grupo")
        else:
            print(f"❌ Erro ao buscar rotas: {rotas_response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar grupo: {str(e)}")
        return False

def main():
    print("🧪 TESTE DE UPLOAD DE PLANILHAS")
    print("="*60)
    
    # Verificar se os arquivos existem
    arquivos_teste = [
        ("base km - Copia.xlsx", "base_km_teste.xlsx"),
        ("BASE MELI - Copia.xlsx", "base_meli_teste.xlsx")
    ]
    
    grupo_id = 3  # Usar grupo ID 3 para teste
    
    for arquivo_original, nome_upload in arquivos_teste:
        if os.path.exists(arquivo_original):
            print(f"\n✅ Arquivo encontrado: {arquivo_original}")
            
            # Testar upload
            sucesso = testar_upload_arquivo(arquivo_original, nome_upload, grupo_id)
            
            if sucesso:
                # Verificar grupo após upload
                verificar_grupo(grupo_id)
            else:
                print(f"❌ Falha no teste do arquivo: {arquivo_original}")
        else:
            print(f"❌ Arquivo não encontrado: {arquivo_original}")
    
    print(f"\n{'='*60}")
    print("🏁 TESTE CONCLUÍDO")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
