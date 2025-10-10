#!/usr/bin/env python3
import requests
import json

def test_api_response_structure():
    print("=== ANÁLISE COMPLETA DA ESTRUTURA DA API ===")
    
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
    
    # Coordenadas São Paulo -> Rio de Janeiro
    pontos = "-46.6333,-23.5505;-43.1729,-22.9068"
    
    try:
        url = f"https://rotasbrasil.com.br/roterizador/buscaRota/?pontos={pontos}&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29"
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print("=== ESTRUTURA COMPLETA DA RESPOSTA ===")
            print(f"Chaves principais: {list(data.keys())}")
            
            if 'routes' in data and data['routes']:
                route = data['routes'][0]
                print(f"\nChaves da rota: {list(route.keys())}")
                
                # Verificar se há campos relacionados a custos
                print(f"\n=== CAMPOS RELACIONADOS A CUSTOS ===")
                for key in route.keys():
                    if any(word in key.lower() for word in ['cost', 'price', 'fee', 'total', 'valor', 'custo', 'preco']):
                        print(f"Campo relacionado: {key} = {route[key]}")
                
                # Verificar se há campos numéricos que possam ser custos
                print(f"\n=== CAMPOS NUMÉRICOS ===")
                for key, value in route.items():
                    if isinstance(value, (int, float)) and value > 0:
                        print(f"Campo numérico: {key} = {value}")
                
                # Verificar se há campos que contenham arrays com valores monetários
                print(f"\n=== CAMPOS COM ARRAYS ===")
                for key, value in route.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"Campo array: {key} (tamanho: {len(value)})")
                        if len(value) > 0 and isinstance(value[0], (int, float)):
                            print(f"  Primeiro valor: {value[0]}")
                        elif len(value) > 0 and isinstance(value[0], list) and len(value[0]) > 0:
                            print(f"  Primeiro sub-array: {value[0][:5]}...")
                
                # Verificar se há campos que contenham strings com valores monetários
                print(f"\n=== CAMPOS COM STRINGS ===")
                for key, value in route.items():
                    if isinstance(value, str) and any(char.isdigit() for char in value):
                        print(f"Campo string: {key} = {value}")
                
                # Salvar resposta completa para análise
                with open('api_response_sp_rj_complete.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n[OK] Resposta salva em 'api_response_sp_rj_complete.json'")
                
            else:
                print("Estrutura de resposta inesperada")
        else:
            print(f"Erro na requisição: {response.status_code}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_api_response_structure()
