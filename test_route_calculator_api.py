#!/usr/bin/env python3
import requests
import json

def test_route_calculator_api():
    print("=== TESTE DA API DE CALCULADORA DE ROTAS ===")
    
    # Testar rota individual
    print("\n1. Testando rota individual...")
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json={
            "origem": "São Paulo, Sao Paulo, BR",
            "destino": "Rio de Janeiro, Rio de Janeiro, BR"
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota individual calculada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destino: {result.get('destino', 'N/A')}")
            print(f"  Distância: {result.get('distance', 'N/A')} km")
            print(f"  Pedágios: R$ {result.get('pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
        else:
            print(f"[ERRO] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")
    
    # Testar rota múltipla
    print("\n2. Testando rota múltipla...")
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate-multiple", json={
            "origem": "São Paulo, Sao Paulo, BR",
            "destinos": ["Campinas, Sao Paulo, BR", "Santos, Sao Paulo, BR"]
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Rota múltipla calculada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destinos: {result.get('destinos', 'N/A')}")
            print(f"  Distância total: {result.get('total_distance', 'N/A')} km")
            print(f"  Pedágios totais: R$ {result.get('total_pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
        else:
            print(f"[ERRO] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")
    
    # Testar sugestões
    print("\n3. Testando sugestões de cidades...")
    try:
        response = requests.get("http://localhost:8000/api/v1/suggestions?termo=São Paulo")
        
        if response.status_code == 200:
            suggestions = response.json()
            print(f"[OK] {len(suggestions)} sugestões encontradas para 'São Paulo'")
            for i, suggestion in enumerate(suggestions[:3], 1):
                print(f"  {i}. {suggestion.get('nome', 'N/A')} - {suggestion.get('endereco_completo', 'N/A')}")
        else:
            print(f"[ERRO] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se todos os testes passaram, a API está funcionando corretamente")
    print(f"e o frontend pode ser testado!")

if __name__ == "__main__":
    test_route_calculator_api()
