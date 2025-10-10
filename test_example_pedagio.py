#!/usr/bin/env python3

def test_example_pedagio():
    print("=== TESTE COM EXEMPLO REAL ===")
    print("Exemplo: Guarulhos -> Jundiaí")
    
    # Exemplo fornecido pelo usuário
    example_pedagio = [
        288,
        "-23.32291",
        "-46.82324",
        0,
        "AUTOBAN",
        "Campo Limpo",
        "SP-348",
        "39,047",
        13.0,
        52774.16457208513,
        1,
        None,
        1,
        "Todos os dias"
    ]
    
    print(f"Pedágio de exemplo:")
    print(f"  ID: {example_pedagio[0]}")
    print(f"  Nome: {example_pedagio[5]}")
    print(f"  Concessionária: {example_pedagio[4]}")
    print(f"  Rodovia: {example_pedagio[6]}")
    print(f"  Valor bruto: '{example_pedagio[7]}'")
    
    # Aplicar a lógica corrigida
    valor_str = str(example_pedagio[7])
    valor_float = float(valor_str.replace(',', '.'))
    
    print(f"\nResultado:")
    print(f"  Valor convertido: R$ {valor_float:.2f}")
    print(f"  Interpretação: {valor_str} -> {valor_float}")
    
    # Verificar se faz sentido
    if 30 <= valor_float <= 50:
        print(f"  [OK] Valor parece correto para um pedágio!")
    else:
        print(f"  [INFO] Valor pode estar incorreto")
    
    print(f"\n=== TESTE COM MÚLTIPLOS PEDÁGIOS ===")
    
    # Simular múltiplos pedágios
    example_pedagios = [
        [288, "-23.32291", "-46.82324", 0, "AUTOBAN", "Campo Limpo", "SP-348", "39,047", 13.0, 52774.16457208513, 1, None, 1, "Todos os dias"],
        [289, "-23.32291", "-46.82324", 0, "AUTOBAN", "Outro Pedágio", "SP-348", "25,500", 13.0, 52774.16457208513, 1, None, 1, "Todos os dias"],
        [290, "-23.32291", "-46.82324", 0, "AUTOBAN", "Mais Um", "SP-348", "15,750", 13.0, 52774.16457208513, 1, None, 1, "Todos os dias"]
    ]
    
    total = 0.0
    for i, pedagio in enumerate(example_pedagios):
        valor_str = str(pedagio[7])
        valor_float = float(valor_str.replace(',', '.'))
        total += valor_float
        print(f"  Pedágio {i+1}: {pedagio[5]} - R$ {valor_float:.2f}")
    
    print(f"\nTotal: R$ {total:.2f}")
    print(f"Valor esperado: ~R$ 80-100 para 3 pedágios")
    
    if 80 <= total <= 100:
        print(f"[OK] Total parece correto!")
    else:
        print(f"[INFO] Total pode estar incorreto")

if __name__ == "__main__":
    test_example_pedagio()
