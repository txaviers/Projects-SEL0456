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
        #Transforma-se a string em uma lista de caracteres 
        self.lt_dados = list(self.dados)     
        #Flag para não mudar vírgulas de dados entre aspas  
        flag_aspas = False

        #Percorre-se cada caracter do conteúdo
        for i in range(len(self.lt_dados)):            
            if not flag_aspas:
                #Caso seja identificado uma primeira aspa, levanta-se a flag
                if self.lt_dados[i] == '"':
                    flag_aspas = True        
                #Enquanto a flag estiver desligada, os separadores são mudados
                elif self.lt_dados[i] == separador_atual:                    
                    self.lt_dados[i] = novo_separador
            #Identificada a última aspa de um dos dados, abaixa-se a flag
            elif self.lt_dados[i] == '"' and flag_aspas:
                flag_aspas = False   
        
        #Transforma-se a lista de caracteres novamente em string
        self.dados = ''.join(self.lt_dados)

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
