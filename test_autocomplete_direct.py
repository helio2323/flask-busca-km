#!/usr/bin/env python3
import requests
import urllib.parse

def test_autocomplete_direct():
    print("=== TESTE DIRETO DA API DE AUTOCOMPLETE ===")
    
    # Headers para a API
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://rotasbrasil.com.br/",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    base_url = "https://rotasbrasil.com.br/apiRotas/autocomplete/"
    
    # Testar diferentes formatos para AGUAI
    test_queries = [
        "AGUAI",
        "Aguai",
        "aguai",
        "AGUAI Sao Paulo",
        "Aguai Sao Paulo",
        "aguai sao paulo",
        "AGUAI, Sao Paulo",
        "Aguai, Sao Paulo"
    ]
    
    for query in test_queries:
        print(f"\nTestando query: '{query}'")
        try:
            url = f"{base_url}?q={urllib.parse.quote(query)}&limit=10"
            print(f"URL: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Resultados encontrados: {len(data)}")
                
                if data:
                    print("Primeiros resultados:")
                    for i, result in enumerate(data[:3], 1):
                        cidade = result.get('cidade', 'N/A')
                        estado = result.get('estado', 'N/A')
                        lat = result.get('lat', 'N/A')
                        lon = result.get('lon', 'N/A')
                        print(f"  {i}. {cidade}, {estado} - Lat: {lat}, Lon: {lon}")
                        
                        # Verificar se é AGUAI
                        if 'aguai' in cidade.lower():
                            print(f"    [OK] ENCONTRADA AGUAI!")
                else:
                    print("Nenhum resultado encontrado")
            else:
                print(f"Erro na requisição: {response.text}")
                
        except Exception as e:
            print(f"Erro: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se nenhuma query encontrou AGUAI, então:")
    print(f"1. A cidade pode não existir na base do Rotas Brasil")
    print(f"2. O nome pode estar diferente (ex: AGUAI vs AGUAÍ)")
    print(f"3. A API pode ter mudado")

if __name__ == "__main__":
    test_autocomplete_direct()
