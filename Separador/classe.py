class Frases():
    def __init__(self, filename:str):

        self.file = open(filename,'r')
        self.dados = self.file.read()  
   
    def mudar_separador(self,separador_atual:str,novo_separador:str):

        self.lt_dados = list(self.dados)       
        flag_aspas = False

        for i in range(len(self.lt_dados)):

            if not flag_aspas:
                if self.lt_dados[i] == '"':
                    flag_aspas = True        
                elif self.lt_dados[i] == separador_atual:                    
                    self.lt_dados[i] = novo_separador

            elif self.lt_dados[i] == '"' and flag_aspas:
                flag_aspas = False   

        print(''.join(self.lt_dados))               
        

if __name__ == '__main__':

    frases_curtas = Frases('arquivo_dados.txt')
    frases_curtas.mudar_separador(",",";")


