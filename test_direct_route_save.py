#!/usr/bin/env python3
import requests

def test_direct_route_save():
    print("=== TESTANDO SALVAMENTO DIRETO DE ROTA ===")
    
    grupo_id = 35
    
    # Testar salvamento direto de uma rota
    print(f"\n1. Testando salvamento direto de rota para grupo {grupo_id}...")
    try:
        test_data = {
            "origem": "Campinas, Sao Paulo, BR",
            "destino": "Adamantina, Sao Paulo, BR"
        }
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota calculada:")
            print(f"  Distância: {result.get('distance', 'N/A')} km")
            print(f"  Pedágios: R$ {result.get('pedagios', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao calcular rota: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao calcular rota: {e}")
        return
    
    # Verificar se a rota foi salva no banco
    print(f"\n2. Verificando se a rota foi salva...")
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
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")
    
    # Verificar estatísticas gerais
    print(f"\n3. Verificando estatísticas gerais...")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] Estatísticas gerais:")
            print(f"  Total de rotas: {stats.get('total_rotas', 'N/A')}")
            print(f"  Distância total: {stats.get('total_distancia', 'N/A')} km")
        else:
            print(f"[ERRO] Erro ao buscar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar estatísticas: {e}")

if __name__ == "__main__":
    test_direct_route_save()
