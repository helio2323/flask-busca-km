#!/usr/bin/env python3
import requests
import json

def test_frontend_input():
    print("=== TESTE DO INPUT DO FRONTEND ===")
    
    # Testar se conseguimos acessar a página
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend acessível")
            
            # Verificar se há algum erro no console
            if "error" in response.text.lower():
                print("[AVISO] Possíveis erros encontrados na página")
            else:
                print("[OK] Página carregada sem erros aparentes")
        else:
            print(f"[ERRO] Frontend retornou status {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro ao acessar frontend: {e}")
    
    # Testar API de sugestões
    print("\n--- Testando API de sugestões ---")
    try:
        response = requests.get("http://localhost:8000/api/v1/suggestions?termo=teste", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API de sugestões funcionando: {len(data.get('sugestoes', []))} sugestões")
        else:
            print(f"[ERRO] API de sugestões retornou status {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro na API de sugestões: {e}")

if __name__ == "__main__":
    test_frontend_input()
