#!/usr/bin/env python3
import requests
import json

def check_database():
    print("=== VERIFICANDO BANCO DE DADOS ===")
    
    # Verificar todas as consultas
    print("\n1. Verificando todas as consultas:")
    try:
        response = requests.get("http://localhost:8000/api/v1/history")
        if response.status_code == 200:
            data = response.json()
            consultas = data.get('consultas', [])
            print(f"Total de consultas no banco: {len(consultas)}")
            
            if consultas:
                print("\nÚltimas 3 consultas:")
                for i, consulta in enumerate(consultas[:3]):
                    print(f"Consulta {i+1}:")
                    print(f"  ID: {consulta.get('id', 'N/A')}")
                    print(f"  Grupo ID: {consulta.get('grupo_id', 'N/A')}")
                    print(f"  Origem: {consulta.get('origem', 'N/A')}")
                    print(f"  Destino: {consulta.get('destino', 'N/A')}")
                    print(f"  Distância: {consulta.get('distancia', 'N/A')} km")
                    print(f"  Pedágios: R$ {consulta.get('pedagios', 'N/A')}")
                    print(f"  Data: {consulta.get('data_consulta', 'N/A')}")
                    print()
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")
    
    # Verificar grupos
    print("\n2. Verificando grupos:")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups")
        if response.status_code == 200:
            data = response.json()
            grupos = data.get('grupos', [])
            print(f"Total de grupos: {len(grupos)}")
            
            for grupo in grupos:
                print(f"Grupo {grupo.get('id', 'N/A')}: {grupo.get('nome', 'N/A')} - {grupo.get('total_rotas', 0)} rotas")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    check_database()
