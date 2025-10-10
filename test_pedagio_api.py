#!/usr/bin/env python3
import requests
import urllib.parse

def test_pedagio_api():
    print("=== TESTE DA API DE PEDÁGIOS ===")
    
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
    
    # Testar rota específica: Campinas -> Adamantina
    origem = "Campinas, Sao Paulo, BR"
    destino = "Adamantina, Sao Paulo, BR"
    
    print(f"Testando rota: {origem} -> {destino}")
    
    # URL da API de rotas (baseada no exemplo_retorno_km.json)
    base_url = "https://rotasbrasil.com.br/roterizador/buscaRota/"
    
    # Parâmetros da API
    params = {
        "pontos": "-47.0608,-22.9056;-50.0731,-21.6856",  # Coordenadas de Campinas e Adamantina
        "alternatives": "true",
        "eixos": "2",
        "veiculo": "1",
        "st": "false",
        "combustivel": "",
        "consumo": "",
        "evitarPedagio": "false",
        "recaptchaRespostaCliente": "03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29"
    }
    
    try:
        url = f"{base_url}?pontos={params['pontos']}&alternatives={params['alternatives']}&eixos={params['eixos']}&veiculo={params['veiculo']}&st={params['st']}&combustivel={params['combustivel']}&consumo={params['consumo']}&evitarPedagio={params['evitarPedagio']}&recaptchaRespostaCliente={params['recaptchaRespostaCliente']}&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29"
        
        print(f"URL: {url[:200]}...")
        
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Resposta recebida com sucesso!")
            
            # Verificar estrutura da resposta
            if 'routes' in data and data['routes']:
                route = data['routes'][0]
                print(f"\nDados da rota:")
                print(f"  Distance: {route.get('distance', 'N/A')}")
                print(f"  Duration: {route.get('duration', 'N/A')}")
                
                # Verificar pedágios
                if 'pedagios' in route:
                    pedagios = route['pedagios']
                    print(f"  Pedágios (raw): {pedagios}")
                    print(f"  Tipo: {type(pedagios)}")
                    
                    if pedagios:
                        print(f"  Pedágios encontrados: {len(pedagios)}")
                        for i, pedagio in enumerate(pedagios):
                            print(f"    Pedágio {i+1}: {pedagio}")
                    else:
                        print(f"  Nenhum pedágio encontrado")
                else:
                    print(f"  Campo 'pedagios' não encontrado na resposta")
                
                # Verificar outros campos relacionados a pedágio
                for key in route.keys():
                    if 'pedagio' in key.lower() or 'toll' in key.lower():
                        print(f"  Campo relacionado a pedágio: {key} = {route[key]}")
            else:
                print(f"Estrutura de resposta inesperada: {data}")
        else:
            print(f"Erro na requisição: {response.text}")
            
    except Exception as e:
        print(f"Erro: {e}")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Se a API não retorna pedágios, então o problema está na API.")
    print(f"Se retorna mas está zerado, então o problema está no processamento.")

if __name__ == "__main__":
    test_pedagio_api()

