#!/usr/bin/env python3
import requests
import json

def test_guarulhos_recife():
    print("=== TESTE GUARULHOS -> RECIFE ===")
    print("Testando rota: Guarulhos, São Paulo -> Recife, Pernambuco")
    
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
    
    # Coordenadas aproximadas
    # Guarulhos: -46.5333, -23.4538
    # Recife: -34.8811, -8.0476
    pontos = "-46.5333,-23.4538;-34.8811,-8.0476"
    
    try:
        url = f"https://rotasbrasil.com.br/roterizador/buscaRota/?pontos={pontos}&alternatives=true&eixos=2&veiculo=1&st=false&combustivel=&consumo=&evitarPedagio=false&recaptchaRespostaCliente=03AFcWeA7j9naH_X1GiW2hXsNijAAl6OD4BGA4Ivh1_OyCx6W_v0z9EU26aLcc5pBUAh7-4RtMF16tD2fXZD-2A2pjC5DkhCEjsvhAnAss5WiYyTJbVc9_s-ggLNMRBIEWu8ZQW1AfHPqCSbKXkQ4XZhCxFgAzYzmF8udZAfhNEI7T6L6Jvcc6vF2ONx-ax9pIJAxmTz3OAFjy4dWCaGCMD9qwb17Fmxm44JP7EiCHm3lRdd_RGGWLQpUagh5gRix6x2U6R0CPffZ1uBpOv3oeM1pSjz0Eoutl_9HUB0nVJQNHIj7huLHV7wpIVj0B2VY5LvuHhh94ysYnWLu9-IqhLihEgOIVlgfjoCae5p0Yl2cUcmwHyyakjjbKpavnD2jfbkPFA97YQ2wcLBOFV6OqtkZ-dceO1yMIo1pp-PEXH7gz2j0QIFB-c8H158UzpacH-27tf8N1Ithk-88ckLZM3U2a1uAgQUhxYDm4Db3ZRFvyT_wydTfFZBGPgSTV1f2-ahy88wEhzxjPkeY7nTo1UNMZcrjnmiau9g--83jPyQSvlUi31MwUobR8AIHRkysOqMctf6WGtwZl9zSCPfurXU-9f95OTK9BZMnTxHpLl_G_7JwZAVc4bdDwh5BSGxPRKnBbeFdaus462FQckgFrtH3aH6Bb4fA_wBIKa5umFMy3xSbXhIXmumPpzUCtXLEyEl30cbrdConCE9_BvoMXwsXqD52bRqONT7rH_KzthaTT0DgE1Eb9x5U&recaptchaRespostaV3=true&evitarBalsa=false&meioPagamento=&fornecedorPagamento=&dataTarifa=2024-02-29"
        
        print(f"Fazendo requisição para a API...")
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Resposta recebida com sucesso!")
            
            if 'routes' in data and data['routes']:
                route = data['routes'][0]
                
                # Informações básicas
                distance_km = route.get('distance', 0) / 1000
                duration_min = route.get('duration', 0) / 60
                
                print(f"\n=== INFORMAÇÕES DA ROTA ===")
                print(f"Distância: {distance_km:.1f} km")
                print(f"Duração: {duration_min:.1f} min ({duration_min/60:.1f} horas)")
                
                # Processar pedágios
                if 'pedagios' in route and route['pedagios']:
                    pedagios = route['pedagios']
                    print(f"\n=== PEDÁGIOS ENCONTRADOS ===")
                    print(f"Total de pedágios: {len(pedagios)}")
                    
                    total_pedagios = 0.0
                    print(f"\nDetalhes dos pedágios:")
                    print(f"{'Nº':<3} {'Nome':<25} {'Concessionária':<15} {'Rodovia':<10} {'Valor':<10}")
                    print(f"{'-'*3} {'-'*25} {'-'*15} {'-'*10} {'-'*10}")
                    
                    for i, pedagio in enumerate(pedagios):
                        if isinstance(pedagio, list) and len(pedagio) > 7:
                            nome = pedagio[5]
                            concessionaria = pedagio[4]
                            rodovia = pedagio[6]
                            valor_str = str(pedagio[7])
                            
                            # Aplicar a lógica corrigida
                            try:
                                valor_float = float(valor_str.replace(',', '.'))
                                total_pedagios += valor_float
                                
                                print(f"{i+1:<3} {nome[:24]:<25} {concessionaria[:14]:<15} {rodovia[:9]:<10} R$ {valor_float:>6.2f}")
                            except (ValueError, TypeError) as e:
                                print(f"{i+1:<3} {nome[:24]:<25} {concessionaria[:14]:<15} {rodovia[:9]:<10} ERRO: {e}")
                    
                    print(f"\n=== RESUMO ===")
                    print(f"Total de pedágios: R$ {total_pedagios:.2f}")
                    print(f"Distância total: {distance_km:.1f} km")
                    print(f"Custo por km: R$ {total_pedagios/distance_km:.3f}/km")
                    
                    # Verificar se o valor faz sentido
                    if total_pedagios > 0:
                        print(f"\n[OK] Pedágios calculados com sucesso!")
                        if 50 <= total_pedagios <= 200:
                            print(f"[OK] Valor parece razoável para uma rota longa")
                        elif total_pedagios < 50:
                            print(f"[INFO] Valor baixo para uma rota tão longa")
                        else:
                            print(f"[INFO] Valor alto, mas pode estar correto")
                    else:
                        print(f"[ERRO] Nenhum pedágio válido encontrado!")
                else:
                    print(f"\n[INFO] Nenhum pedágio encontrado para esta rota")
                
                # Salvar resposta para análise
                with open('guarulhos_recife_response.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n[OK] Resposta salva em 'guarulhos_recife_response.json'")
                
            else:
                print(f"[ERRO] Estrutura de resposta inesperada")
        else:
            print(f"[ERRO] Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")

if __name__ == "__main__":
    test_guarulhos_recife()
