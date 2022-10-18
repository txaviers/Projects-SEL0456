import re

#Implementa-se a classe proposta para manipular arquivo
class ArquivoTXT():
    def __init__(self, filename:str):
        self.file = open(filename,'r')   #arquivo txt
        self.dados = self.file.read()    #conteúdo string do arquivo texto  

    #Método de impressão da classe: print do conteúdo do arquivo txt
    def __str__(self):
        S = "\nARQUIVO DE DADOS TEXTO:\n\n"
        S += self.dados   
        return S

    #Método para mudar o separador
    def mudar_separador(self, separador_atual:str, novo_separador:str):
        #Expressão regular para identificar separador fora de dados com aspas
        regex_expression = separador_atual + '(?=(?:[^"]|"[^"]*")*$)'    
        self.dados = re.sub(regex_expression, novo_separador, self.dados)

    #Método para salvar o contéudo no mesmo ou em um novo arquivo
    def salvar_arquivo(self, filename:str):        
        self.saved_file = open(filename,'w')
        self.saved_file.write(self.dados)
        self.saved_file.close()

if __name__ == '__main__':
    #Programa principal

    #Define-se uma variável da classe criada
    dados = ArquivoTXT("arquivo_dados.txt")
    print(dados)

    #Muda-se o separador dos dados
    dados.mudar_separador(",",";")
    print(dados)
    
    #Salvam-se os novos dados em um novo arquivo
    dados.salvar_arquivo("arquivo_dados_modif.txt")
