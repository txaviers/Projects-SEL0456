# Função para encontrar o n-ésimo termo da Seq. de Fibonacci começando por 0
def fibonacci(n:int):
    return fibonacci(n-1) + fibonacci(n-2) if n > 1 else n

# Função para calcular o fatorial de n
def fatorial(n:int):
    return n*fatorial(n-1) if n != 0 else 1

# Conversão do formato de dados do arquivo (colunas) para uma lista de listas
def list_parse(conteudo:str):
    lista = []
    for linha in conteudo.splitlines():
        try:
            lista.append(list(map(int, linha.split())))
        except ValueError:
            pass     

    return lista

# Conversão de retorno de lista de listas para o formato de dados do arquivo .dat (duas colunas)
def two_column_parse(lt:list):
    S = ''
    for par in lt:
        S += str(par[0]) + ' ' + str(par[1]) + '\n'
    return S

