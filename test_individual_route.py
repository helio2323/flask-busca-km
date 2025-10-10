#!/usr/bin/env python3
import requests
import json

def test_individual_route():
    print("=== TESTANDO ROTA INDIVIDUAL ===")
    
    # Testar uma rota simples
    rota_data = {
        "origem": "CAMPINAS, São Paulo, BR",
        "destino": "ADAMANTINA, São Paulo, BR"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=rota_data)
        if response.status_code == 200:
            resultado = response.json()
            print("Rota calculada com sucesso:")
            print(f"Origem: {resultado.get('origem', 'N/A')}")
            print(f"Destino: {resultado.get('destino', 'N/A')}")
            print(f"Distância: {resultado.get('distance', 'N/A')} km")
            print(f"Pedágios: R$ {resultado.get('pedagios', 'N/A')}")
            print(f"Fonte: {resultado.get('fonte', 'N/A')}")
        else:
            print(f"Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_individual_route()
