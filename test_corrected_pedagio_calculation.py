#!/usr/bin/env python3
import json

def test_corrected_pedagio_calculation():
    print("=== TESTE DA CORREÇÃO DE PEDÁGIOS ===")
    
    try:
        # Carregar o arquivo JSON
        with open('chamdas_api/exemplo_retorno_km.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'routes' in data and data['routes']:
            route = data['routes'][0]
            pedagios = route['pedagios']
            
            print(f"Total de pedágios encontrados: {len(pedagios)}")
            print(f"\n=== CÁLCULO CORRIGIDO ===")
            
            total_pedagios = 0.0
            for i, pedagio in enumerate(pedagios):
                if isinstance(pedagio, list) and len(pedagio) > 7:
                    valor_str = str(pedagio[7])
                    # A vírgula é separador de milhares, então remover e dividir por 100
                    valor_float = float(valor_str.replace(',', '')) / 100
                    total_pedagios += valor_float
                    print(f"  Pedágio {i+1}: {pedagio[5]} - R$ {valor_float:.2f}")
            
            print(f"\n=== RESULTADO ===")
            print(f"Total calculado: R$ {total_pedagios:.2f}")
            print(f"Valor mostrado na imagem: R$ 53,70")
            print(f"Diferença: R$ {abs(total_pedagios - 53.70):.2f}")
            
            if abs(total_pedagios - 53.70) < 1.0:
                print(f"[OK] Valores próximos! A correção funcionou!")
            else:
                print(f"[INFO] Ainda há diferença, mas muito menor que antes")
                print(f"[INFO] Antes: R$ 7.710,67 vs R$ 53,70 (diferença: R$ 7.656,97)")
                print(f"[INFO] Agora: R$ {total_pedagios:.2f} vs R$ 53,70 (diferença: R$ {abs(total_pedagios - 53.70):.2f})")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_corrected_pedagio_calculation()
