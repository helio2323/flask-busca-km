#!/usr/bin/env python3
import requests
import pandas as pd

def test_specific_routes():
    print("=== TESTANDO ROTAS ESPECÍFICAS ===")
    
    # Testar as rotas do arquivo rotas.xlsx
    test_cases = [
        {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "ADAMANTINA, Sao Paulo, BR"},
        {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "ADOLFO, Sao Paulo, BR"},
        {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "AGUAI, Sao Paulo, BR"},
        {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "AGUAS DA PRATA, Sao Paulo, BR"},
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTeste {i+1}: {test_case['origem']} -> {test_case['destino']}")
        try:
            response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_case)
            if response.status_code == 200:
                result = response.json()
                distance = result.get('distance', 0)
                pedagios = result.get('pedagios', 0)
                
                print(f"[OK] Distância: {distance} km, Pedágios: R$ {pedagios}")
                
                # Verificar se seria considerado válido
                distancia_valida = isinstance(distance, (int, float)) and distance > 0
                pedagios_validos = isinstance(pedagios, (int, float)) and pedagios >= 0
                
                print(f"  Distância válida: {distancia_valida}")
                print(f"  Pedágios válidos: {pedagios_validos}")
                print(f"  Resultado seria salvo: {distancia_valida and pedagios_validos}")
                
            else:
                print(f"[ERRO] {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[ERRO] {e}")

if __name__ == "__main__":
    test_specific_routes()
