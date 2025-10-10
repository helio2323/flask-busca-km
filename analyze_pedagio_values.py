#!/usr/bin/env python3
import json

def analyze_pedagio_values():
    print("=== ANÁLISE DETALHADA DOS VALORES DE PEDÁGIOS ===")
    
    try:
        # Carregar o arquivo JSON
        with open('chamdas_api/exemplo_retorno_km.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'routes' in data and data['routes']:
            route = data['routes'][0]
            pedagios = route['pedagios']
            
            print("Valores brutos dos pedágios:")
            print("=" * 50)
            
            for i, pedagio in enumerate(pedagios):
                if isinstance(pedagio, list) and len(pedagio) > 7:
                    valor_bruto = pedagio[7]
                    nome = pedagio[5]
                    
                    print(f"Pedágio {i+1}: {nome}")
                    print(f"  Valor bruto: '{valor_bruto}'")
                    print(f"  Tamanho: {len(valor_bruto)} caracteres")
                    print(f"  Contém vírgula: {',' in valor_bruto}")
                    print(f"  Posição da vírgula: {valor_bruto.find(',') if ',' in valor_bruto else 'N/A'}")
                    
                    # Tentar diferentes interpretações
                    try:
                        # Interpretação atual (vírgula como separador decimal)
                        valor_atual = float(valor_bruto.replace(',', '.'))
                        print(f"  Interpretação atual: R$ {valor_atual}")
                        
                        # Interpretação alternativa (vírgula como separador de milhares)
                        if ',' in valor_bruto:
                            partes = valor_bruto.split(',')
                            if len(partes) == 2:
                                # Se tem 2 partes, pode ser decimal ou milhares
                                if len(partes[1]) == 3:  # 3 dígitos após vírgula = milhares
                                    valor_alternativo = float(partes[0] + partes[1]) / 100
                                    print(f"  Interpretação alternativa (milhares): R$ {valor_alternativo}")
                                else:  # 1-2 dígitos após vírgula = decimal
                                    print(f"  Interpretação alternativa (decimal): R$ {valor_atual}")
                    except ValueError as e:
                        print(f"  Erro na conversão: {e}")
                    
                    print()
            
            # Calcular total com interpretação atual
            total_atual = 0.0
            for pedagio in pedagios:
                if isinstance(pedagio, list) and len(pedagio) > 7:
                    try:
                        valor = float(pedagio[7].replace(',', '.'))
                        total_atual += valor
                    except ValueError:
                        pass
            
            print(f"Total com interpretação atual: R$ {total_atual:.2f}")
            print(f"Valor mostrado na imagem: R$ 53,70")
            print(f"Diferença: R$ {total_atual - 53.70:.2f}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    analyze_pedagio_values()
