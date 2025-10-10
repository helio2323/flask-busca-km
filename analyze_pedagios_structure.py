#!/usr/bin/env python3

def analyze_pedagios_structure():
    print("=== ANÁLISE DA ESTRUTURA DE PEDÁGIOS ===")
    
    # Dados fornecidos pelo usuário
    pedagios_data = [
        [306, "-23.322352548022803", "-46.581178628484736", 0, "FERNÃO DIAS", "P1-Mairiporã", "BR-381", "65,700", 2.9, 23282.67656283354, 1, None, 1, "Todos os dias"],
        [220, "-22.90875435603499", "-46.424773029430355", 1, "FERNÃO DIAS", "P2-Vargem", "BR-381", "7,200", 2.9, 79734.76930765893, 1, None, 1, "Todos os dias"],
        [222, "-22.628616655340547", "-46.07786665641402", 1, "FERNÃO DIAS", "P3-Cambuí", "BR-381", "900,900", 2.9, 134753.48506505135, 1, None, 1, "Todos os dias"],
        [298, "-21.97039243866623", "-45.630801174274495", 1, "FERNÃO DIAS", "P4-São Gonçalo do Sapucaí", "BR-381", "805,200", 2.9, 228367.9975789074, 1, None, 1, "Todos os dias"],
        [96, "-21.54571660410512", "-45.24017049321935", 1, "FERNÃO DIAS", "P5-Carmo da Cachoeira", "BR-381", "735,500", 2.9, 298209.9005132605, 1, None, 1, "Todos os dias"],
        [301, "-21.00028817097447", "-44.966784746032715", 1, "FERNÃO DIAS", "P6-Santo Antônio do Amparo", "BR-381", "658,300", 2.9, 374243.9836328697, 1, None, 1, "Todos os dias"],
        [295, "-20.591839549010643", "-44.70124586991801", 1, "FERNÃO DIAS", "P7-Carmópolis de Minas", "BR-381", "597,700", 2.9, 433817.2364663287, 1, None, 1, "Todos os dias"],
        [47, "-20.268340333984753", "-44.4238126548334", 1, "FERNÃO DIAS", "P8-Itatiaiuçú", "BR-381", "545,900", 2.9, 484813.40863216884, 1, None, 1, "Todos os dias"],
        [57, "-15.232413391113452", "-41.1010013726671", 1, "VIABAHIA", "P7-Vitória da Conquista", "BR-116", "873,499", 6.1, 1344120.46111787, 1, None, 1, "Todos os dias"],
        [383, "-14.646179570468776", "-40.45583825756546", 1, "VIABAHIA", "P6-Planalto", "BR-116", "773,819", 6.1, 1444556.4690894356, 1, None, 1, "Todos os dias"],
        [69, "-14.056012554743884", "-40.20424015381269", 1, "VIABAHIA", "P5-Jequié", "BR-116", "698,410", 6.1, 1519560.421284105, 1, None, 1, "Todos os dias"],
        [399, "-13.008716945137529", "-39.95717653200762", 1, "VIABAHIA", "P4-Brejões/Nova Itarana", "BR-116", "566,405", 6.1, 1651912.3439255175, 1, None, 1, "Todos os dias"],
        [398, "-12.531889324723664", "-39.41504884540376", 1, "VIABAHIA", "P3-Rafael Jambeiro", "BR-116", "482,138", 6.1, 1736489.9422218888, 1, None, 1, "Todos os dias"]
    ]
    
    print(f"Total de pedágios: {len(pedagios_data)}")
    print(f"\n=== ANÁLISE DETALHADA ===")
    
    # Testar diferentes interpretações
    print(f"\n1. INTERPRETAÇÃO ATUAL (vírgula como decimal):")
    total1 = 0.0
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        valor_float = float(valor_str.replace(',', '.'))
        total1 += valor_float
        print(f"  {i+1:2d}. {pedagio[5][:20]:<20} - {valor_str:<8} -> R$ {valor_float:>7.2f}")
    print(f"  TOTAL: R$ {total1:.2f}")
    
    print(f"\n2. INTERPRETAÇÃO ALTERNATIVA (vírgula como milhares):")
    total2 = 0.0
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        valor_float = float(valor_str.replace(',', ''))
        total2 += valor_float
        print(f"  {i+1:2d}. {pedagio[5][:20]:<20} - {valor_str:<8} -> R$ {valor_float:>7.2f}")
    print(f"  TOTAL: R$ {total2:.2f}")
    
    print(f"\n3. INTERPRETAÇÃO ALTERNATIVA (vírgula como milhares / 100):")
    total3 = 0.0
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        valor_float = float(valor_str.replace(',', '')) / 100
        total3 += valor_float
        print(f"  {i+1:2d}. {pedagio[5][:20]:<20} - {valor_str:<8} -> R$ {valor_float:>7.2f}")
    print(f"  TOTAL: R$ {total3:.2f}")
    
    print(f"\n=== ANÁLISE DOS PADRÕES ===")
    
    # Analisar padrões nos valores
    print(f"\nValores brutos:")
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        print(f"  {i+1:2d}. {valor_str}")
    
    # Verificar se há padrão na posição da vírgula
    print(f"\nPosição da vírgula:")
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        pos_virgula = valor_str.find(',')
        print(f"  {i+1:2d}. {valor_str} - vírgula na posição {pos_virgula}")
    
    # Verificar se há padrão no número de dígitos após a vírgula
    print(f"\nDígitos após a vírgula:")
    for i, pedagio in enumerate(pedagios_data):
        valor_str = str(pedagio[7])
        if ',' in valor_str:
            partes = valor_str.split(',')
            digitos_apos = len(partes[1])
            print(f"  {i+1:2d}. {valor_str} - {digitos_apos} dígitos após vírgula")
        else:
            print(f"  {i+1:2d}. {valor_str} - sem vírgula")
    
    print(f"\n=== CONCLUSÃO ===")
    print(f"Interpretação 1 (decimal): R$ {total1:.2f}")
    print(f"Interpretação 2 (milhares): R$ {total2:.2f}")
    print(f"Interpretação 3 (milhares/100): R$ {total3:.2f}")
    print(f"\nQual interpretação faz mais sentido para pedágios?")

if __name__ == "__main__":
    analyze_pedagios_structure()
