#!/usr/bin/env python3
import requests

def test_atualizar_estatisticas():
    print("=== TESTE DA FUNÇÃO ATUALIZAR_ESTATÍSTICAS ===")
    
    # Vou testar com um grupo existente
    grupo_id = 43  # Grupo do teste anterior
    
    print(f"\n1. Verificando grupo {grupo_id} antes da atualização...")
    try:
        response = requests.get(f"http://localhost:8000/api/v1/groups/{grupo_id}")
        if response.status_code == 200:
            grupo_info = response.json()
            grupo_data = grupo_info.get('grupo', {})
            print(f"[OK] Grupo encontrado:")
            print(f"  Nome: {grupo_data.get('nome', 'N/A')}")
            print(f"  Total de rotas: {grupo_data.get('total_rotas', 'N/A')}")
            print(f"  Distancia total: {grupo_data.get('total_distancia', 'N/A')} km")
            print(f"  Pedagios totais: R$ {grupo_data.get('total_pedagios', 'N/A')}")
            print(f"  Status: {grupo_data.get('status', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar grupo: {response.status_code}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao buscar grupo: {e}")
        return
    
    # 2. Verificar estatísticas gerais
    print(f"\n2. Verificando estatísticas gerais...")
    try:
        response = requests.get("http://localhost:8000/api/v1/groups/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] Estatísticas gerais:")
            print(f"  Total de grupos: {stats.get('total_grupos', 'N/A')}")
            print(f"  Total de rotas: {stats.get('total_rotas', 'N/A')}")
            print(f"  Distancia total: {stats.get('total_distancia', 'N/A')} km")
            print(f"  Pedagios totais: R$ {stats.get('total_pedagios', 'N/A')}")
        else:
            print(f"[ERRO] Erro ao buscar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar estatísticas: {e}")
    
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
                for i, rota in enumerate(rotas, 1):
                    print(f"  {i}. {rota.get('origem', 'N/A')} -> {rota.get('destino', 'N/A')}")
                    print(f"     Distancia: {rota.get('distancia', 'N/A')} km")
                    print(f"     Pedagios: R$ {rota.get('pedagios', 'N/A')}")
                    print(f"     Data: {rota.get('data_consulta', 'N/A')}")
                    print()
            else:
                print("Nenhuma rota encontrada no grupo")
        else:
            print(f"[ERRO] Erro ao buscar rotas: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao buscar rotas: {e}")
    
    print(f"\n=== DIAGNÓSTICO ===")
    print(f"Se as estatísticas gerais mostram rotas mas o grupo não tem rotas,")
    print(f"então há um problema na função atualizar_estatisticas_grupo.")
    print(f"Possíveis causas:")
    print(f"1. A função não está sendo chamada")
    print(f"2. A função está sendo chamada mas há erro na query")
    print(f"3. As consultas estão sendo salvas sem grupo_id")
    print(f"4. Há problema na transação do banco de dados")

if __name__ == "__main__":
    test_atualizar_estatisticas()
