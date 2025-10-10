#!/usr/bin/env python3
import requests

def check_database_directly():
    print("=== VERIFICANDO BANCO DE DADOS DIRETAMENTE ===")
    
    grupo_id = 35  # ID do último teste
    
    # 1. Verificar se há consultas no banco
    print("\n1. Verificando consultas no banco...")
    try:
        # Tentar buscar todas as consultas
        response = requests.get("http://localhost:8000/api/v1/groups/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] Estatísticas gerais:")
            print(f"  Total de grupos: {stats.get('total_grupos', 'N/A')}")
            print(f"  Total de rotas: {stats.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {stats.get('total_distancia', 'N/A')} km")
            print(f"  Pedágios totais: R$ {stats.get('total_pedagios', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar estatísticas: {e}")
    
    # 2. Verificar grupo específico
    print(f"\n2. Verificando grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Grupo encontrado:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {grupo_data.get('total_distancia', 'N/A')} km")
            print(f"  Pedágios totais: R$ {grupo_data.get('total_pedagios', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")
    
    # 3. Verificar se há consultas com grupo_id
    print(f"\n3. Verificando consultas do grupo {grupo_id}...")
    try:
        # Tentar buscar rotas do grupo
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            
            if rotas:
                print("\nRotas encontradas:")
                for i, rota in enumerate(rotas):
                    print(f"  {i+1}. {rota.get('origem')} -> {rota.get('destino')} ({rota.get('distancia')} km, R$ {rota.get('pedagios')})")
            else:
                print("Nenhuma rota encontrada no grupo")
        else:
            print(f"[ERRO] Erro ao buscar rotas do grupo: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas do grupo: {e}")
    
    # 4. Verificar erros de upload
    print(f"\n4. Verificando erros de upload...")
    try:
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
            print(f"[ERRO] Erro ao buscar erros: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar erros: {e}")

if __name__ == "__main__":
    check_database_directly()
