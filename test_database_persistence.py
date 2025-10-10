#!/usr/bin/env python3
import requests

def test_database_persistence():
    print("=== TESTANDO PERSISTÊNCIA NO BANCO ===")
    
    grupo_id = 36  # ID do último teste
    
    # 1. Verificar estatísticas gerais
    print("\n1. Verificando estatísticas gerais...")
    try:
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
    
    # 3. Verificar rotas do grupo
    print(f"\n3. Verificando rotas do grupo {grupo_id}...")
    try:
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
    
    # 4. Testar uma rota individual para ver se é salva
    print(f"\n4. Testando rota individual...")
    try:
        test_data = {
            "origem": "Campinas, Sao Paulo, BR",
            "destino": "Adamantina, Sao Paulo, BR"
        }
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota individual calculada:")
            print(f"  Distância: {result.get('distance', 'N/A')} km")
            print(f"  Pedágios: R$ {result.get('pedagios', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao calcular rota individual: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao calcular rota individual: {e}")
    
    # 5. Verificar se a rota individual foi salva
    print(f"\n5. Verificando se a rota individual foi salva...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo após rota individual")
            
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

if __name__ == "__main__":
    test_database_persistence()
