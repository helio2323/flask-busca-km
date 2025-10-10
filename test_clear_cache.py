#!/usr/bin/env python3
import requests
import json
import time

def test_clear_cache():
    print("=== TESTANDO LIMPEZA DE CACHE ===")
    
    # Testar rota individual
    test_route = {
        "origem": "Campinas, Sao Paulo, BR",
        "destino": "Adamantina, Sao Paulo, BR"
    }
    
    print(f"Testando rota: {test_route['origem']} -> {test_route['destino']}")
    
    try:
        # Fazer múltiplas tentativas para ver se há cache
        for i in range(3):
            print(f"\n--- Tentativa {i+1} ---")
            
            # Adicionar timestamp para evitar cache
            test_route_with_time = test_route.copy()
            test_route_with_time['timestamp'] = time.time()
            
            response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_route_with_time)
            if response.status_code == 200:
                result = response.json()
                print(f"[OK] Rota individual testada:")
                print(f"  Origem: {result.get('origem', 'N/A')}")
                print(f"  Destino: {result.get('destino', 'N/A')}")
                print(f"  Distancia: {result.get('distance', 'N/A')} km")
                print(f"  Pedagios: R$ {result.get('pedagios', 'N/A')}")
                print(f"  Fonte: {result.get('fonte', 'N/A')}")
                
                # Verificar se há dados brutos
                if 'raw_data' in result:
                    print(f"  [OK] Dados brutos presentes na resposta")
                    raw_data = result['raw_data']
                    if 'routes' in raw_data and raw_data['routes']:
                        route = raw_data['routes'][0]
                        print(f"    Distance: {route.get('distance', 'N/A')}")
                        print(f"    Duration: {route.get('duration', 'N/A')}")
                        print(f"    Pedágios (raw): {route.get('pedagios', 'N/A')}")
                        print(f"    Tipo de pedágios: {type(route.get('pedagios', 'N/A'))}")
                        
                        # Verificar se a condição está sendo atendida
                        print(f"\n[DEBUG] Verificando condição:")
                        print(f"    'pedagios' in route: {'pedagios' in route}")
                        print(f"    route['pedagios']: {route.get('pedagios', 'N/A')}")
                        print(f"    bool(route['pedagios']): {bool(route.get('pedagios', []))}")
                        
                        if 'pedagios' in route and route['pedagios']:
                            print(f"    [OK] Condição atendida - processando pedágios")
                        else:
                            print(f"    [INFO] Condição não atendida - pedágios = 0.0")
                    else:
                        print(f"    [ERRO] Estrutura de dados inesperada")
                else:
                    print(f"  [INFO] Sem dados brutos na resposta - possível cache")
                    
                # Verificar se há mensagens de debug
                print(f"\n[DEBUG] Verificando se há mensagens de debug:")
                print(f"  Resposta completa: {json.dumps(result, indent=2, ensure_ascii=False)}")
            else:
                print(f"[ERRO] Erro ao testar rota individual: {response.status_code}")
                print(f"Resposta: {response.text}")
            
            time.sleep(1)  # Aguardar 1 segundo entre tentativas
    except Exception as e:
        print(f"[ERRO] Erro ao testar rota individual: {e}")
    
    print(f"\n=== DIAGNÓSTICO ===")
    print(f"Se não há dados brutos em nenhuma tentativa, então:")
    print(f"1. O servidor não foi reiniciado com as mudanças")
    print(f"2. Há cache sendo usado")
    print(f"3. A correção não está sendo aplicada")
    print(f"4. O endpoint está usando uma versão antiga do código")

if __name__ == "__main__":
    test_clear_cache()

