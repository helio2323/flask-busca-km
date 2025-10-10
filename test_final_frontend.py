#!/usr/bin/env python3
import requests
import json

def test_final_frontend():
    print("=== TESTE FINAL DO FRONTEND ===")
    
    print("1. Verificando se o frontend está rodando...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend acessível")
        else:
            print(f"[ERRO] Frontend retornou status {response.status_code}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao acessar frontend: {e}")
        return
    
    print("\n2. Verificando se o backend está rodando...")
    try:
        response = requests.get("http://localhost:8000/api/v1/suggestions?termo=teste", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend acessível")
        else:
            print(f"[ERRO] Backend retornou status {response.status_code}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao acessar backend: {e}")
        return
    
    print("\n3. Testando API de sugestões...")
    try:
        response = requests.get("http://localhost:8000/api/v1/suggestions?termo=campinas", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API de sugestões funcionando: {len(data.get('sugestoes', []))} sugestões")
        else:
            print(f"[ERRO] API de sugestões retornou status {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro na API de sugestões: {e}")
    
    print("\n4. Testando API de cálculo de rota...")
    try:
        response = requests.post("http://localhost:8000/api/v1/routes/calculate", json={
            "origem": "São Paulo, Sao Paulo, BR",
            "destino": "Rio de Janeiro, Rio de Janeiro, BR"
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API de cálculo funcionando: {data.get('distance', 'N/A')} km, R$ {data.get('pedagios', 'N/A')}")
        else:
            print(f"[ERRO] API de cálculo retornou status {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro na API de cálculo: {e}")
    
    print(f"\n=== INSTRUÇÕES PARA TESTE MANUAL ===")
    print(f"1. Acesse: http://localhost:3000")
    print(f"2. Vá para a aba 'Calcular Rota'")
    print(f"3. Tente digitar no primeiro input (Origem)")
    print(f"4. Verifique o console do navegador (F12) para ver os logs")
    print(f"5. Se aparecer 'Input 1 mudou para: ...' no console, o input está funcionando")
    print(f"6. Se não aparecer nada, há um problema no React")

if __name__ == "__main__":
    test_final_frontend()
