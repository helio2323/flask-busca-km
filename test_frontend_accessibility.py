#!/usr/bin/env python3
import requests
import json

def test_frontend_accessibility():
    print("=== TESTE DE ACESSIBILIDADE DO FRONTEND ===")
    
    # Testar se o frontend está rodando
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend está rodando na porta 3000")
        else:
            print(f"[ERRO] Frontend retornou status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[ERRO] Frontend não está rodando na porta 3000")
        print("Execute: cd route-frontend && npm run dev")
    except Exception as e:
        print(f"[ERRO] Erro ao acessar frontend: {e}")
    
    # Testar se o backend está rodando
    try:
        response = requests.get("http://localhost:8000/api/v1/suggestions?termo=teste", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend está rodando na porta 8000")
        else:
            print(f"[ERRO] Backend retornou status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[ERRO] Backend não está rodando na porta 8000")
        print("Execute: cd backend && python -m uvicorn app.main:app --reload --port 8000")
    except Exception as e:
        print(f"[ERRO] Erro ao acessar backend: {e}")

if __name__ == "__main__":
    test_frontend_accessibility()
