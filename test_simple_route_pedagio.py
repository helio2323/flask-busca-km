#!/usr/bin/env python3
import requests
import json

def test_simple_route_pedagio():
    print("=== TESTE COM ROTA SIMPLES ===")
    print("Testando rota São Paulo -> Rio de Janeiro (deve ter pedágios conhecidos)")
    
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
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'routes' in data and data['routes']:
                route = data['routes'][0]
                print(f"\nDistância: {route.get('distance', 0) / 1000:.1f} km")
                print(f"Duração: {route.get('duration', 0) / 60:.1f} min")
                
                if 'pedagios' in route:
                    pedagios = route['pedagios']
                    print(f"\nPedágios encontrados: {len(pedagios)}")
                    
                    # Mostrar apenas os primeiros 3 pedágios para análise
                    for i, pedagio in enumerate(pedagios[:3]):
                        if isinstance(pedagio, list) and len(pedagio) > 7:
                            print(f"\nPedágio {i+1}:")
                            print(f"  Nome: {pedagio[5]}")
                            print(f"  Concessionária: {pedagio[4]}")
                            print(f"  Rodovia: {pedagio[6]}")
                            print(f"  Valor bruto: '{pedagio[7]}'")
                            
                            # Testar diferentes interpretações
                            valor_str = str(pedagio[7])
                            try:
                                # Interpretação 1: Vírgula como decimal
                                valor1 = float(valor_str.replace(',', '.'))
                                print(f"  Como decimal: R$ {valor1:.2f}")
                                
                                # Interpretação 2: Vírgula como milhares
                                valor2 = float(valor_str.replace(',', ''))
                                print(f"  Como milhares: R$ {valor2:.2f}")
                                
                                # Interpretação 3: Vírgula como milhares / 100
                                valor3 = float(valor_str.replace(',', '')) / 100
                                print(f"  Como milhares/100: R$ {valor3:.2f}")
                                
                            except ValueError as e:
                                print(f"  Erro na conversão: {e}")
                    
                    # Calcular total com interpretação decimal (mais comum)
                    total_decimal = 0.0
                    for pedagio in pedagios:
                        if isinstance(pedagio, list) and len(pedagio) > 7:
                            try:
                                valor = float(str(pedagio[7]).replace(',', '.'))
                                total_decimal += valor
                            except ValueError:
                                pass
                    
                    print(f"\nTotal com interpretação decimal: R$ {total_decimal:.2f}")
                    print(f"Valor esperado para SP-RJ: ~R$ 50-100")
                    
                    if 50 <= total_decimal <= 100:
                        print(f"[OK] Valor parece correto!")
                    else:
                        print(f"[ERRO] Valor muito diferente do esperado!")
                        
                else:
                    print("Nenhum pedágio encontrado!")
            else:
                print("Estrutura de resposta inesperada")
        else:
            print(f"Erro na requisição: {response.status_code}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_simple_route_pedagio()
