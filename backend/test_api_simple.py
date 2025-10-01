#!/usr/bin/env python3
"""
Teste simples da API
"""

import requests
import time

def test_api():
    print("🧪 Testando API...")
    
    # Aguardar um pouco
    print("⏳ Aguardando 5 segundos...")
    time.sleep(5)
    
    try:
        # Testar health check
        print("🔍 Testando health check...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"✅ Health check: {response.status_code}")
        print(f"📄 Resposta: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - API não está rodando")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    try:
        # Testar documentação
        print("\n🔍 Testando documentação...")
        response = requests.get("http://localhost:8000/docs", timeout=10)
        print(f"✅ Docs: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - API não está rodando")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_api()
