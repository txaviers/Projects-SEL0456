# Importa todas as funções do script do projeto anterior 
from fibfact import *

# Lê o conteúdo do arquivo de teste
arquivo = open('test.dat','r')
dados = arquivo.read()

# Transforma as linhas do arquivo em uma lista de listas
for lista in list_parse(dados):
    # Para cada linha do arquivo de teste, compara as respostas
    try:
        assert fibonacci(lista[0]) == lista[2], "Erro no Fibonacci de " + str(lista[0])
        assert fatorial(lista[0]) == lista[1], "Erro no fatorial de " + str(lista[0])
    except AssertionError as msg:
        # Printa o erro e o índice onde ocorreu
        print(msg)

print("Fim da checagem")

