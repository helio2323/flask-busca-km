#!/usr/bin/env python3
import requests

def test_individual_route_with_autocomplete():
    print("=== TESTE DE ROTA INDIVIDUAL COM AUTOCOMPLETE ===")
    
    # Testar uma rota específica
    test_route = {
        "origem": "Campinas, Sao Paulo, BR",
        "destino": "Adamantina, Sao Paulo, BR"
    }
    
    print(f"Testando rota: {test_route['origem']} -> {test_route['destino']}")
    
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_route)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota calculada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destino: {result.get('destino', 'N/A')}")
            print(f"  Distancia: {result.get('distance', 'N/A')} km")
            print(f"  Pedagios: R$ {result.get('pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
            
            # Verificar se os valores são válidos
            distance = result.get('distance', 0)
            pedagios = result.get('pedagios', 0)
            
            # Converter para float se necessário
            try:
                distance_float = float(distance) if distance is not None else 0
                pedagios_float = float(pedagios) if pedagios is not None else 0
            except (ValueError, TypeError):
                distance_float = 0
                pedagios_float = 0
            
            if distance_float > 0:
                print(f"[OK] Distancia válida: {distance_float} km")
            else:
                print(f"[ERRO] Distancia inválida: {distance_float}")
                
            if pedagios_float >= 0:
                print(f"[OK] Pedagios válidos: R$ {pedagios_float}")
            else:
                print(f"[ERRO] Pedagios inválidos: R$ {pedagios_float}")
                
        else:
            print(f"[ERRO] Erro ao calcular rota: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao calcular rota: {e}")

if __name__ == "__main__":
    test_individual_route_with_autocomplete()
