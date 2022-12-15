import json
from inverse import inversefunc

class TabelasConversao:
    def __init__(self, file):
        self.file = file
        self.data = self.open_file()

    def open_file(self):
        with open(self.file, encoding="utf-8") as json_data_file:
            data = json.load(json_data_file)    
        return data

    def save_file(self, data):
        with open(self.file, 'w', encoding='utf-8') as att_file:
            json.dump(data, att_file, indent=4, ensure_ascii=False) 

    # Método para identificar as medidas possíveis
    def get_medidas(self):       
        self.data = self.open_file()
        return [names for names in self.data.keys()]

    # Método para identificar os elementos do dicionário de uma determinada medida
    def get_json_elements(self, medida):
        self.data = self.open_file()
        # Resultado para medidas calculadas com fatores
        res_fator = [list(t) for t in tuple(self.data[medida].items())]
        # Resultado para medidas calculadas com função
        res_func = []
        
        for item in res_fator:
            # Considera-se, inicialmente, que a medida é feita com fator
            # Se identificado padrão de função, muda-se o resultado de res_fator para res_func
            if "/" in item[0]:
                unidade_in = item[0].split('/', 1)[0]
                unidade_out = item[0].split('/', 1)[1]
                func = eval(item[1])

                res_func.append([unidade_in, unidade_out, func])
                res_func.append([unidade_out, unidade_in, inversefunc(func)])
        
        # Retorna uma flag (True) para identificar medida feita por função e o resultado
        return (False, res_fator) if len(res_func) == 0 else (True, res_func)        

    # Método para identificar o nome das unidades da medida 
    def get_unidades(self, HasFunction, elements):        
        if HasFunction:
            unidades = list(dict.fromkeys([item for sublist in elements for item in sublist[0:2]]))
        else:
            unidades = [item[0] for item in elements]
        
        return unidades

    # Método para identificar o fator de uma medida 
    def get_fator(self, unidade, elements):       
        for item in elements:
            if unidade == item[0]:               
                return item[1]  

    # Método para identificar a função de uma medida 
    def get_function(self, unidade_in, unidade_out, elements):
        for item in elements:
            if unidade_in == item[0] and unidade_out == item[1]:
                return item[2]

    # Método para adicionar nova medida
    def add_medida(self, new_medida:str):        
        if new_medida in self.data:
            return "Medida já configurada!"
        else:      
            if type(self.data) is dict:    
                self.data[new_medida] = {}                
            
            self.save_file (self.data)                
                
            return "Medida adicionada!"

    # Método para remover medida
    def remover_medida(self, medida:str):
        if medida in self.data:
            del self.data[medida]

        self.save_file (self.data)               

    # Método para adicionar fator multiplicativo
    def add_unidade_fator(self, medida, unidade, fator:float):
        if medida in self.data:
            if unidade in self.data[medida]:
                return "Unidade já existe!"
            else:
                self.data[medida][unidade] = fator 

                self.save_file (self.data)          

                return "Unidade adicionada!"

    # Método para adicionar função
    def add_unidade_func(self, medida, unidade_entrada:str, unidade_saída:str, func:str):
        if medida in self.data:
            conversao = unidade_entrada + '/' + unidade_saída

            if conversao in self.data[medida]:
                return "Conversão entre essas unidades já existe!"
            else:
                self.data[medida][conversao] = "lambda X : " + func

                self.save_file(self.data)          

                return "Função adicionada!"

if __name__ == '__main__':

    BDD = TabelasConversao('unidades.json')
    medidas = BDD.get_medidas()

    HasFunction, tab = BDD.get_json_elements(medidas[1])
   
    print(BDD.get_unidades(HasFunction, tab))
    print(BDD.get_function("Celsius", "Kelvin", tab))
    
    print(BDD.add_medida("Teste"))
    
    BDD.add_unidade_fator("Teste", "Teste Unidade", 100)
    BDD.add_unidade_func("Teste", "Teste1", "Teste2", "2*X")

    BDD.remover_medida("Teste")
    print(BDD.get_medidas())