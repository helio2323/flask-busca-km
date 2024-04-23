def ler_valor():
    with open('contagem.txt', 'r') as arquivo:
        return int(arquivo.read())

# Função para atualizar o valor no arquivo
def atualizar_valor(valor):
    with open('contagem.txt', 'w') as arquivo:
        arquivo.write(str(valor))

quantidade = ler_valor()


