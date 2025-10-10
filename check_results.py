#!/usr/bin/env python3
import requests
import json

def check_results():
    print("=== VERIFICANDO RESULTADOS DO TESTE ===")
    
    # 1. Verificar status do upload
    print("\n1. Status do upload:")
    try:
        response = requests.get("http://localhost:8000/api/v1/routes/upload-status/4b4844f8")
        if response.status_code == 200:
            status = response.json()
            print(f"Status: {status['status']}")
            print(f"Total de rotas: {status['total_rotas']}")
            print(f"Rotas processadas: {status['rotas_processadas']}")
            print(f"Rotas com erro: {status['rotas_com_erro']}")
            print(f"Progresso: {status['progresso']}%")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")
    
    # 2. Verificar rotas do grupo
    print("\n2. Rotas do grupo 32:")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups/32/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"Total de rotas encontradas: {len(rotas)}")
            
            for i, rota in enumerate(rotas):
                print(f"\nRota {i+1}:")
                print(f"  Origem: {rota.get('origem', 'N/A')}")
                print(f"  Destino: {rota.get('destino', 'N/A')}")
                print(f"  Distância: {rota.get('distancia', 'N/A')} km")
                print(f"  Pedágios: R$ {rota.get('pedagios', 'N/A')}")
                print(f"  Fonte: {rota.get('fonte', 'N/A')}")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")
    
    # 3. Verificar estatísticas do grupo
    print("\n3. Estatísticas do grupo:")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups/32")
        if response.status_code == 200:
            grupo = response.json()
            print(f"Nome: {grupo.get('nome', 'N/A')}")
            print(f"Total de rotas: {grupo.get('total_rotas', 'N/A')}")
            print(f"Distância total: {grupo.get('total_distancia', 'N/A')} km")
            print(f"Pedágios totais: R$ {grupo.get('total_pedagios', 'N/A')}")
            print(f"Status: {grupo.get('status', 'N/A')}")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    check_results()
