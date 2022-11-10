from fibfact import *

arquivo = open('test.dat','r')
dados = arquivo.read()

conteudo = dados.splitlines()
print(conteudo)

for linha in conteudo:   
    n_columns = len(linha.split())     
    print(linha.split())
    
        