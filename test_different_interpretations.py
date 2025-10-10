#!/usr/bin/env python3

def test_different_interpretations():
    print("=== TESTE DE DIFERENTES INTERPRETAÇÕES ===")
    
    # Dados fornecidos pelo usuário
    pedagios_data = [
        [306, "-23.322352548022803", "-46.581178628484736", 0, "FERNÃO DIAS", "P1-Mairiporã", "BR-381", "65,700", 2.9, 23282.67656283354, 1, None, 1, "Todos os dias"],
        [220, "-22.90875435603499", "-46.424773029430355", 1, "FERNÃO DIAS", "P2-Vargem", "BR-381", "7,200", 2.9, 79734.76930765893, 1, None, 1, "Todos os dias"],
        [222, "-22.628616655340547", "-46.07786665641402", 1, "FERNÃO DIAS", "P3-Cambuí", "BR-381", "900,900", 2.9, 134753.48506505135, 1, None, 1, "Todos os dias"],
        [298, "-21.97039243866623", "-45.630801174274495", 1, "FERNÃO DIAS", "P4-São Gonçalo do Sapucaí", "BR-381", "805,200", 2.9, 228367.9975789074, 1, None, 1, "Todos os dias"],
        [96, "-21.54571660410512", "-45.24017049321935", 1, "FERNÃO DIAS", "P5-Carmo da Cachoeira", "BR-381", "735,500", 2.9, 298209.9005132605, 1, None, 1, "Todos os dias"]
    ]
    
    print("Testando diferentes interpretações com os primeiros 5 pedágios:")
    print(f"{'Nº':<3} {'Nome':<20} {'Valor Bruto':<10} {'/100':<10} {'/1000':<10} {'/10000':<10}")
    print(f"{'-'*3} {'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        valor_num = float(valor_str.replace(',', ''))
        
        valor_100 = valor_num / 100
        valor_1000 = valor_num / 1000
        valor_10000 = valor_num / 10000
        
        print(f"{i+1:2d}. {pedagio[5][:19]:<20} {valor_str:<10} R$ {valor_100:>7.2f} R$ {valor_1000:>7.2f} R$ {valor_10000:>7.2f}")
    
    # Calcular totais para cada interpretação
    print(f"\n=== TOTAIS PARA TODOS OS 13 PEDÁGIOS ===")
    
    total_100 = 0.0
    total_1000 = 0.0
    total_10000 = 0.0
    
    for pedagio in pedagios_data:
        valor_str = str(pedagio[7])
        valor_num = float(valor_str.replace(',', ''))
        
        total_100 += valor_num / 100
        total_1000 += valor_num / 1000
        total_10000 += valor_num / 10000
    
    print(f"Dividindo por 100:   R$ {total_100:.2f}")
    print(f"Dividindo por 1000:  R$ {total_1000:.2f}")
    print(f"Dividindo por 10000: R$ {total_10000:.2f}")
    print(f"Valor da imagem:     R$ 53,70")
    
    # Encontrar a mais próxima
    diffs = [
        ("/100", abs(total_100 - 53.70)),
        ("/1000", abs(total_1000 - 53.70)),
        ("/10000", abs(total_10000 - 53.70))
    ]
    
    mais_proxima = min(diffs, key=lambda x: x[1])
    print(f"\nMais próxima: {mais_proxima[0]} (diferença: R$ {mais_proxima[1]:.2f})")
    
    if mais_proxima[1] < 10:
        print(f"[OK] Encontramos a interpretação correta!")
    else:
        print(f"[INFO] Nenhuma interpretação está próxima de R$ 53,70")
        print(f"[INFO] Talvez o valor da imagem seja de uma fonte diferente")

if __name__ == "__main__":
    test_different_interpretations()