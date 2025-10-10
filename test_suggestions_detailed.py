#!/usr/bin/env python3
import requests
import json

def test_suggestions_api():
    print("=== TESTE DETALHADO DA API DE SUGESTÕES ===")
    
    # Testar diferentes termos
    termos_teste = ["São Paulo", "Rio", "Campinas", "Santos"]
    
    for termo in termos_teste:
        print(f"\n--- Testando termo: '{termo}' ---")
        try:
            response = requests.get(f"http://localhost:8000/api/v1/suggestions?termo={termo}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Status: {response.status_code}")
                print(f"[OK] Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if 'sugestoes' in data:
                    sugestoes = data['sugestoes']
                    print(f"[OK] {len(sugestoes)} sugestões encontradas")
                    for i, sugestao in enumerate(sugestoes[:3], 1):
                        print(f"  {i}. {sugestao.get('nome', 'N/A')} - {sugestao.get('endereco_completo', 'N/A')}")
                else:
                    print(f"[AVISO] Campo 'sugestoes' não encontrado na resposta")
            else:
                print(f"[ERRO] Status: {response.status_code}")
                print(f"[ERRO] Resposta: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"[ERRO] Timeout na requisição para '{termo}'")
        except requests.exceptions.ConnectionError:
            print(f"[ERRO] Erro de conexão para '{termo}'")
        except Exception as e:
            print(f"[ERRO] Erro inesperado para '{termo}': {e}")

if __name__ == "__main__":
    test_suggestions_api()
