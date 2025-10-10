#!/usr/bin/env python3
import requests
import json
import urllib.parse

def test_rotas_brasil_sp_rj():
    print("=== CHAMADA DIRETA PARA API ROTAS BRASIL ===")
    print("Rota: São Paulo -> Rio de Janeiro (deve ter pedágios)")
    
    # Headers baseados no exemplo_retorno_km.json
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
    
    # Coordenadas aproximadas de São Paulo e Rio de Janeiro
    # São Paulo: -46.6333, -23.5505
    # Rio de Janeiro: -43.1729, -22.9068
    pontos = "-46.6333,-23.5505;-43.1729,-22.9068"
    
    # URL da API
    base_url = "https://rotasbrasil.com.br/roterizador/buscaRota/"
    
    try:
        # Construir URL completa
        url = f"{base_url}?pontos={pontos}&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29"
        
        print(f"URL: {url[:200]}...")
        print(f"Fazendo requisição...")
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[OK] Resposta recebida com sucesso!")
            
            # Analisar estrutura da resposta
            print(f"\n=== ESTRUTURA DA RESPOSTA ===")
            print(f"Chaves principais: {list(data.keys())}")
            
            if 'routes' in data and data['routes']:
                route = data['routes'][0]
                print(f"\n=== DADOS DA ROTA ===")
                print(f"Chaves da rota: {list(route.keys())}")
                
                # Informações básicas
                print(f"\nDistance: {route.get('distance', 'N/A')}")
                print(f"Duration: {route.get('duration', 'N/A')}")
                
                # Analisar pedágios
                print(f"\n=== ANÁLISE DE PEDÁGIOS ===")
                print(f"'pedagios' in route: {'pedagios' in route}")
                
                if 'pedagios' in route:
                    pedagios = route['pedagios']
                    print(f"Pedágios (raw): {pedagios}")
                    print(f"Tipo: {type(pedagios)}")
                    
                    if isinstance(pedagios, list):
                        print(f"Lista com {len(pedagios)} itens:")
                        for i, pedagio in enumerate(pedagios):
                            print(f"  Pedágio {i+1}: {pedagio}")
                            print(f"    Tipo: {type(pedagio)}")
                            if isinstance(pedagio, dict):
                                print(f"    Chaves: {list(pedagio.keys())}")
                                for key, value in pedagio.items():
                                    print(f"      {key}: {value}")
                    elif isinstance(pedagios, (int, float)):
                        print(f"Valor numérico: {pedagios}")
                    else:
                        print(f"Tipo inesperado: {pedagios}")
                else:
                    print(f"Campo 'pedagios' não encontrado!")
                
                # Procurar por outras chaves relacionadas a pedágio
                print(f"\n=== PROCURANDO OUTRAS CHAVES DE PEDÁGIO ===")
                for key in route.keys():
                    if 'pedagio' in key.lower() or 'toll' in key.lower() or 'taxa' in key.lower():
                        print(f"Chave relacionada: {key} = {route[key]}")
                
                # Salvar resposta completa para análise
                with open('rotas_brasil_response_sp_rj.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n[OK] Resposta salva em 'rotas_brasil_response_sp_rj.json'")
                
            else:
                print(f"[ERRO] Estrutura de resposta inesperada")
                print(f"Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"[ERRO] Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Analise a estrutura do JSON para identificar:")
    print(f"1. Se há campo 'pedagios'")
    print(f"2. Qual é a estrutura dos pedágios")
    print(f"3. Se há outras chaves relacionadas a pedágio")
    print(f"4. Se o valor está em formato diferente do esperado")

if __name__ == "__main__":
    test_rotas_brasil_sp_rj()
