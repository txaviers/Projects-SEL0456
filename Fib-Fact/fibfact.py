# Função para encontrar o n-ésimo termo da Seq. de Fibonacci começando por 0
def fibonacci(n:int):
    return fibonacci(n-1) + fibonacci(n-2) if n > 1 else n

# Função para calcular o fatorial de n
def fatorial(n:int):
    return n*fatorial(n-1) if n != 0 else 1

# Conversão do formato de dados do arquivo (duas colunas) para uma lista de listas
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

#### PROGRAMA PRINCIPAL ####

# Lê-se o arquivo de dados e salva-se o conteúdo numa variável 
arquivo = open('dados.dat','r')
dados = arquivo.read()

# Transforma-se o conteúdo no formato lista de listas 
par_dados = list_parse(dados)

print(par_dados)

# Cálculos de fibonacci/fatorial
res = [[fibonacci(i[0]), fatorial(i[1])] for i in par_dados]

# Salva-se o resultado num novo arquivo, retornando a lista de listas para o formato de duas colunas
output = open('output.dat','w')
output.write(two_column_parse(res))
output.close()

