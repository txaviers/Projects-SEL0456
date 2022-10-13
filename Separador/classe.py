class Frases():
    def __init__(self, filename:str):

        self.file = open(filename,'r')
        self.dados = self.file.readlines()
        for i in self.dados:
            print(i)

    def mudar_separador(self,separador_atual:str,novo_separador:str):
        pass
        
        

if __name__ == '__main__':

    frases_curtas = Frases('dados.txt')
 


