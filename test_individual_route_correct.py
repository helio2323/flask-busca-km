#!/usr/bin/env python3
import requests

def test_individual_route():
    print("=== TESTANDO ROTA INDIVIDUAL ===")
    
    try:
        test_data = {
            "origem": "Campinas, Sao Paulo, BR",
            "destino": "Adamantina, Sao Paulo, BR"
        }
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_data)
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
    test_individual_route()
