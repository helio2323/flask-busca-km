#!/usr/bin/env python3
import requests
import json

def test_pedagio_calculation_direct():
    print("=== TESTE DIRETO DO CÁLCULO DE PEDÁGIOS ===")
    
    # Simular dados da API do Rotas Brasil (baseado na resposta real)
    mock_route_data = {
        "pedagios": [
            [16, '-23.413006306839865', '-46.36108163558197', 1, 'NOVADUTRA*', 'Arujá N/S', 'BR-116', '204,500', 3.4, 35862.53232991927, 1, None, 1, 'Todos os dias'],
            [1, '-23.34642', '-46.16487', 0, 'NOVADUTRA*', 'Guararema N/S', 'BR-116', '180,000', 3.4, 57748.28214214553, 1, None, 1, 'Todos os dias'],
            [8, '-23.296446564865718', '-46.00744273134785', 1, 'NOVADUTRA*', 'Jacareí', 'BR-116', '165,000', 6.2, 75047.24470021315, 1, None, 1, 'Todos os dias'],
            [5, '-22.93023452140059', '-45.360851069940566', 1, 'NOVADUTRA*', 'Moreira César', 'BR-116', '88,000', 13.0, 153164.59559426137, 1, None, 1, 'Todos os dias'],
            [12, '-22.49488142012463', '-44.56958427976224', 1, 'NOVADUTRA*', 'Itatiaia', 'BR-116', '318,000', 11.1, 254824.51559936462, 1, None, 1, 'Todos os dias'],
            [6, '-22.716286706484418', '-43.71675908465579', 1, 'ECORIOMINAS', 'P4 - Viúva Graça', 'BR-116', '207,000', 15.1, 366996.55394164904, 1, None, 1, 'Todos os dias']
        ]
    }
    
    print("Dados simulados da API:")
    print(f"Total de pedágios: {len(mock_route_data['pedagios'])}")
    
    # Aplicar a lógica de cálculo corrigida
    pedagios = 0.0
    if 'pedagios' in mock_route_data and mock_route_data['pedagios']:
        try:
            if isinstance(mock_route_data['pedagios'], list):
                print(f"\nProcessando pedágios:")
                for i, pedagio in enumerate(mock_route_data['pedagios']):
                    if isinstance(pedagio, list) and len(pedagio) > 7:
                        valor_str = str(pedagio[7])  # Posição 7: valor do pedágio
                        # Converter vírgula para ponto e depois para float
                        valor_float = float(valor_str.replace(',', '.'))
                        pedagios += valor_float
                        print(f"  Pedágio {i+1}: {pedagio[5]} - R$ {valor_float}")
            elif isinstance(mock_route_data['pedagios'], (int, float)):
                pedagios = float(mock_route_data['pedagios'])
        except (ValueError, TypeError, IndexError) as e:
            print(f"Erro ao processar pedágios: {e}")
            pedagios = 0.0
    
    print(f"\nTotal de pedágios calculados: R$ {pedagios}")
    
    # Verificar se o cálculo está correto
    print(f"\n=== VERIFICAÇÃO ===")
    print(f"Valores esperados:")
    print(f"  Arujá N/S: R$ 204,50")
    print(f"  Guararema N/S: R$ 180,00")
    print(f"  Jacareí: R$ 165,00")
    print(f"  Moreira César: R$ 88,00")
    print(f"  Itatiaia: R$ 318,00")
    print(f"  P4 - Viúva Graça: R$ 207,00")
    print(f"  Total esperado: R$ 1162,50")
    print(f"  Total calculado: R$ {pedagios}")
    
    if abs(pedagios - 1162.50) < 0.01:
        print(f"  [OK] Cálculo correto!")
    else:
        print(f"  [ERRO] Cálculo incorreto!")

if __name__ == "__main__":
    test_pedagio_calculation_direct()
