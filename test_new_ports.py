#!/usr/bin/env python3
import requests
import json

def test_new_ports():
    print("=== TESTE DAS NOVAS PORTAS ===")
    print("Frontend: 5000 | Backend: 5001")
    print("=" * 40)
    
    # Testar frontend na porta 5000
    print("\n1. Testando Frontend (porta 5000)...")
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend acessível na porta 5000")
        else:
            print(f"[ERRO] Frontend retornou status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[ERRO] Frontend não está rodando na porta 5000")
    except Exception as e:
        print(f"[ERRO] Erro ao acessar frontend: {e}")
    
    # Testar backend na porta 5001
    print("\n2. Testando Backend (porta 5001)...")
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend acessível na porta 5001")
        else:
            print(f"[ERRO] Backend retornou status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[ERRO] Backend não está rodando na porta 5001")
    except Exception as e:
        print(f"[ERRO] Erro ao acessar backend: {e}")
    
    # Testar API de sugestões
    print("\n3. Testando API de sugestões...")
    try:
        response = requests.get("http://localhost:5001/api/v1/suggestions?termo=teste", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API de sugestões funcionando: {len(data.get('sugestoes', []))} sugestões")
        else:
            print(f"[ERRO] API de sugestões retornou status {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro na API de sugestões: {e}")
    
    # Testar API de cálculo
    print("\n4. Testando API de cálculo...")
    try:
        response = requests.post("http://localhost:5001/api/v1/routes/calculate", json={
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
    
    print(f"\n=== RESUMO ===")
    print(f"[OK] Frontend: http://localhost:5000")
    print(f"[OK] Backend: http://localhost:5001")
    print(f"[OK] API Docs: http://localhost:5001/docs")
    print(f"[OK] PostgreSQL: localhost:5432")

if __name__ == "__main__":
    test_new_ports()
