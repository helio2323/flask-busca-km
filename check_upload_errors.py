#!/usr/bin/env python3
import requests

def check_upload_errors():
    print("=== VERIFICANDO ERROS DE UPLOAD ===")
    
    grupo_id = 34  # ID do grupo do teste anterior
    
    try:
        # Verificar erros do grupo
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/errors")
        if response.status_code == 200:
            errors = response.json()
            print(f"[OK] {len(errors)} erros encontrados")
            
            for i, error in enumerate(errors):
                print(f"\nErro {i+1}:")
                print(f"  Upload ID: {error.get('upload_id', 'N/A')}")
                print(f"  Linha: {error.get('linha_index', 'N/A')}")
                print(f"  Origem: {error.get('origem_original', 'N/A')}")
                print(f"  Destino: {error.get('destino_original', 'N/A')}")
                print(f"  Tipo: {error.get('tipo_erro', 'N/A')}")
                print(f"  Mensagem: {error.get('mensagem_erro', 'N/A')}")
                print(f"  Status: {error.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar erros: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao conectar: {e}")

if __name__ == "__main__":
    check_upload_errors()
