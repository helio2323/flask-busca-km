#!/usr/bin/env python3
import requests
import json
import time

def test_restart_backend():
    print("=== TESTANDO REINICIALIZAÇÃO DO BACKEND ===")
    
    print("O problema é que o servidor backend não foi reiniciado com as mudanças.")
    print("A correção está no código, mas o servidor está usando a versão antiga.")
    print("\nPara resolver:")
    print("1. Pare o servidor backend (Ctrl+C)")
    print("2. Reinicie o servidor backend")
    print("3. Teste novamente")
    
    print("\n=== TESTANDO ROTA INDIVIDUAL ===")
    
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
                print(f"  [OK] Dados brutos presentes na resposta")
                print(f"  [OK] Correção está sendo aplicada!")
            else:
                print(f"  [INFO] Sem dados brutos na resposta")
                print(f"  [ERRO] Correção NÃO está sendo aplicada!")
                print(f"  [SOLUÇÃO] Reinicie o servidor backend")
        else:
            print(f"[ERRO] Erro ao testar rota individual: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"[ERRO] Erro ao testar rota individual: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se não há dados brutos, então o servidor precisa ser reiniciado.")
    print(f"A correção está no código, mas não está sendo aplicada.")

if __name__ == "__main__":
    test_restart_backend()

