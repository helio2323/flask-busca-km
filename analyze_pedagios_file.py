#!/usr/bin/env python3
import json

def analyze_pedagios_from_file():
    print("=== ANÁLISE DOS PEDÁGIOS DO ARQUIVO EXEMPLO ===")
    
    try:
        # Carregar o arquivo JSON
        with open('chamdas_api/exemplo_retorno_km.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Arquivo carregado com sucesso!")
        
        # Encontrar a seção de pedágios
        if 'routes' in data and data['routes']:
            route = data['routes'][0]
            print(f"\nEstrutura da rota: {list(route.keys())}")
            
            if 'pedagios' in route:
                pedagios = route['pedagios']
                print(f"\nTotal de pedágios encontrados: {len(pedagios)}")
                
                # Analisar cada pedágio
                total_pedagios = 0.0
                print(f"\n=== ANÁLISE DETALHADA DOS PEDÁGIOS ===")
                
                for i, pedagio in enumerate(pedagios):
                    if isinstance(pedagio, list) and len(pedagio) > 7:
                        # Estrutura: [id, lat, lon, tipo, concessionaria, nome, rodovia, valor, ?, ?, ?, ?, ?, dias]
                        id_pedagio = pedagio[0]
                        lat = pedagio[1]
                        lon = pedagio[2]
                        tipo = pedagio[3]
                        concessionaria = pedagio[4]
                        nome = pedagio[5]
                        rodovia = pedagio[6]
                        valor_str = pedagio[7]  # Posição 7: valor do pedágio
                        
                        # Converter valor
                        try:
                            valor_float = float(valor_str.replace(',', '.'))
                            total_pedagios += valor_float
                            
                            print(f"  Pedágio {i+1}:")
                            print(f"    ID: {id_pedagio}")
                            print(f"    Nome: {nome}")
                            print(f"    Concessionária: {concessionaria}")
                            print(f"    Rodovia: {rodovia}")
                            print(f"    Valor: R$ {valor_float}")
                            print(f"    Coordenadas: {lat}, {lon}")
                            print()
                        except (ValueError, TypeError) as e:
                            print(f"  Erro ao processar pedágio {i+1}: {e}")
                            print(f"  Valor: {valor_str}")
                            print()
                    else:
                        print(f"  Pedágio {i+1}: Estrutura inesperada - {pedagio}")
                
                print(f"=== TOTAL CALCULADO ===")
                print(f"Total de pedágios: R$ {total_pedagios:.2f}")
                print(f"Valor mostrado na imagem: R$ 53,70")
                print(f"Diferença: R$ {total_pedagios - 53.70:.2f}")
                
                # Verificar se há outros campos relacionados a pedágio
                print(f"\n=== OUTROS CAMPOS RELACIONADOS ===")
                for key in route.keys():
                    if 'pedagio' in key.lower() or 'toll' in key.lower() or 'taxa' in key.lower() or 'custo' in key.lower():
                        print(f"Campo relacionado: {key} = {route[key]}")
                
            else:
                print("Campo 'pedagios' não encontrado!")
        else:
            print("Estrutura de dados inesperada!")
            
    except Exception as e:
        print(f"Erro ao analisar arquivo: {e}")

if __name__ == "__main__":
    analyze_pedagios_from_file()
