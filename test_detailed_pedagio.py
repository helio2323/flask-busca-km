#!/usr/bin/env python3
import requests
import json

def test_detailed_pedagio():
    print("=== TESTE DETALHADO DE PEDÁGIOS ===")
    
    # Testar rota individual
    test_route = {
        "origem": "Campinas, Sao Paulo, BR",
        "destino": "Adamantina, Sao Paulo, BR"
    }
    
    print(f"Testando rota: {test_route['origem']} -> {test_route['destino']}")
    
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_route)
        if response.status_code == 200:
            result = response.json()
            print(f"\n[OK] Rota individual testada:")
            print(f"  Origem: {result.get('origem', 'N/A')}")
            print(f"  Destino: {result.get('destino', 'N/A')}")
            print(f"  Distancia: {result.get('distance', 'N/A')} km")
            print(f"  Pedagios: R$ {result.get('pedagios', 'N/A')}")
            print(f"  Fonte: {result.get('fonte', 'N/A')}")
            
            # Verificar se há dados brutos
            if 'raw_data' in result:
                raw_data = result['raw_data']
                print(f"\n[DATA] Dados brutos da API:")
                if 'routes' in raw_data and raw_data['routes']:
                    route = raw_data['routes'][0]
                    print(f"  Distance: {route.get('distance', 'N/A')}")
                    print(f"  Duration: {route.get('duration', 'N/A')}")
                    print(f"  Pedágios (raw): {route.get('pedagios', 'N/A')}")
                    print(f"  Tipo de pedágios: {type(route.get('pedagios', 'N/A'))}")
                    
                    # Verificar estrutura dos pedágios
                    pedagios = route.get('pedagios', [])
                    if isinstance(pedagios, list):
                        print(f"  Pedágios é uma lista com {len(pedagios)} itens")
                        for i, pedagio in enumerate(pedagios):
                            print(f"    Pedágio {i+1}: {pedagio} (tipo: {type(pedagio)})")
                    else:
                        print(f"  Pedágios não é uma lista: {pedagios}")
                    
                    # Verificar se a condição está sendo atendida
                    print(f"\n[DEBUG] Verificando condição:")
                    print(f"  'pedagios' in route: {'pedagios' in route}")
                    print(f"  route['pedagios']: {route.get('pedagios', 'N/A')}")
                    print(f"  bool(route['pedagios']): {bool(route.get('pedagios', []))}")
                    
                    if 'pedagios' in route and route['pedagios']:
                        print(f"  [OK] Condição atendida - processando pedágios")
                    else:
                        print(f"  [INFO] Condição não atendida - pedágios = 0.0")
                else:
                    print(f"  [ERRO] Estrutura de dados inesperada")
            else:
                print(f"  [INFO] Sem dados brutos na resposta")
        else:
            print(f"[ERRO] Erro ao testar rota individual: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao testar rota individual: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se a condição não está sendo atendida, então a API")
    print(f"realmente não retorna pedágios para essa rota específica.")

if __name__ == "__main__":
    test_detailed_pedagio()

