#!/usr/bin/env python3
import requests
import pandas as pd

def debug_group_issue():
    print("=== DEBUGANDO PROBLEMA DO GRUPO ===")
    
    grupo_id = 34
    
    # 1. Verificar se há consultas no banco
    print("\n1. Verificando consultas no banco...")
    try:
        response = requests.get("http://localhost:8000/api/v1/routes/history")
        if response.status_code == 200:
            history = response.json()
            print(f"[OK] {len(history)} consultas no histórico")
            
            # Filtrar consultas recentes
            recent_consultas = [c for c in history if 'Campinas' in c.get('origem', '')]
            print(f"[OK] {len(recent_consultas)} consultas com Campinas")
            
            if recent_consultas:
                print("\nÚltimas consultas com Campinas:")
                for i, consulta in enumerate(recent_consultas[:3]):
                    print(f"  {i+1}. {consulta.get('origem')} -> {consulta.get('destino')} ({consulta.get('distancia')} km)")
        else:
            print(f"[ERRO] Erro ao buscar histórico: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar histórico: {e}")
    
    # 2. Verificar grupo diretamente
    print(f"\n2. Verificando grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Grupo encontrado:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")
    
    # 3. Verificar rotas do grupo
    print(f"\n3. Verificando rotas do grupo {grupo_id}...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}/rotas")
        if response.status_code == 200:
            data = response.json()
            rotas = data.get('rotas', [])
            print(f"[OK] {len(rotas)} rotas encontradas no grupo")
            
            if rotas:
                print("\nRotas encontradas:")
                for i, rota in enumerate(rotas[:3]):
                    print(f"  {i+1}. {rota.get('origem')} -> {rota.get('destino')} ({rota.get('distancia')} km)")
        else:
            print(f"[ERRO] Erro ao buscar rotas do grupo: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas do grupo: {e}")
    
    # 4. Verificar se há problema na concatenação
    print(f"\n4. Testando concatenação manual...")
    try:
        # Testar com dados do arquivo
        test_cases = [
            {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "ADAMANTINA, Sao Paulo, BR"},
            {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "ADOLFO, Sao Paulo, BR"},
            {"origem": "CAMPINAS, Sao Paulo, BR", "destino": "AGUAI, Sao Paulo, BR"},
        ]
        
        for i, test_case in enumerate(test_cases):
            response = requests.post("http://localhost:8000/api/v1/routes/calculate", json=test_case)
            if response.status_code == 200:
                result = response.json()
                print(f"[OK] Teste {i+1}: {result.get('distance', 'N/A')} km")
            else:
                print(f"[ERRO] Teste {i+1}: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro nos testes: {e}")

if __name__ == "__main__":
    debug_group_issue()
