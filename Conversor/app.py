# Scripts de funções auxiliares
from func import *
from config_handler import *

# Biblioteca
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib 

CONFIG_FILE = 'config.json'

# Classe do aplicativo
class Main_App_Window(Gtk.Window):
    def __init__(self):        
        self.builder = Gtk.Builder()        
        self.builder.add_from_file('main_window.glade')         # Glade XML
        self.config = TabelasConversao(CONFIG_FILE)        # Dados de conversão 
        self.inicializaçao = True                              # Flag para indicar init

        # Flag para identificar entry em alteração (evita recursão)
        self.flag_changing_entry1 = False       

        # Objetos do app
        self.window = self.builder.get_object('window')                
        self.entry1 = self.builder.get_object('entry1')
        self.entry2 = self.builder.get_object('entry2')
        self.combo_medidas = self.builder.get_object('combo_medidas')
        self.combo1 = self.builder.get_object('combo1')
        self.combo2 = self.builder.get_object('combo2')

        # Opções das Combo Box                     
        self.unidades = Gtk.ListStore(str)
        self.tipos_de_medidas = Gtk.ListStore(str)  

        # Inicializa a primeira Combo Box com os tipos de medidas da BDD
        self.combo_medida_config()

        # Configuração Combo Box para tipos de medidas        
        self.select_medida(self.combo_medidas)  
        self.changed_combo1(self.combo1)
        self.changed_combo2(self.combo2)

        self.builder.connect_signals(self)
        self.window.show_all()         

    def delete_window(self, widget):               
        Gtk.main_quit()

    def activate_help_window(self, widget):                 
        gui = Help_Window()          
        Gtk.main()
        
    def activate_adicionar_medida(self,widget):       
        gui = Add_Medida_Window()        
        Gtk.main()          
        self.combo_medida_config()
    
    def activate_remover_medida(self,widget):       
        gui = Remover_Medida_Window()        
        Gtk.main()          
        self.combo_medida_config()
       
    def activate_add_unidade(self, widget):
        gui = Add_Unidade_Window()   
        Gtk.main()                 
        self.select_medida(self.combo_medidas)       

    def combo_medida_config(self):
        self.tipos_de_medidas.clear()

        for medidas in self.config.get_medidas():                      
            self.tipos_de_medidas.append([medidas])   
        
        self.combo_config(self.combo_medidas, self.tipos_de_medidas, 0)

    # Método de configuração de uma Combo Box
    def combo_config(self, combo, liststore, i): 
        combo.clear()
        combo.set_model(liststore)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)          
        combo.add_attribute(renderer_text, "text", i)         
        combo.set_active(0)   

    # Método para identificar tipo de medida selecionado e atualizar as Combo Box de unidades (1 e 2)
    def select_medida(self, widget):  
        # Reset nas entries      
        self.entry1.set_sensitive(True)
        self.entry2.set_sensitive(True)
        self.entry1.set_text('')        
        self.entry2.set_text('')                

        model = widget.get_model()
        active = widget.get_active()

        if active >= 0:
            # Extrai o tipo de medida selecionado
            medida = model[active][0]                  
            # Reseta a lista de opções das Combo Box de unidade 
            self.unidades.clear()               

            # Identifica se a medida é calculada por função e extrai a tabela de conversão (unidades+fator/função)
            self.HasFunction, self.tab = self.config.get_json_elements(medida)
            
            # Extrai as unidades da tabela d conversão e adiciona na ListStore das Combo Box de unidade
            for item in self.config.get_unidades(self.HasFunction, self.tab):                 
                self.unidades.append([item])                         
                
            # Configuração das Combo Box de unidades
            self.combo_config(self.combo1, self.unidades, 0)
            self.combo_config(self.combo2, self.unidades, 0)         

            if len(self.unidades) == 0:     
                self.entry1.set_sensitive(False)
                self.entry2.set_sensitive(False)      
                
    # Métodos para mudança na Combo Box de unidade
    def changed_combo1(self,widget):     
        # Quando uma opção é selecionada, identifica-se a unidade escolhida   
        model = widget.get_model()
        active = widget.get_active()

        if active >= 0:            
            self.unidade1 = model[active][0]     

        # Não faz-se nada na abertura do aplicativo
        if not self.inicializaçao:            
            self.flag_changing_entry1 = True            
            self.changed_entry1(self.entry1)
       
    def changed_combo2(self, widget):
        model = widget.get_model()
        active = widget.get_active()

        if active >= 0:            
            self.unidade2 = model[active][0]                  
            
        if not self.inicializaçao:
            self.flag_changing_entry2 = True            
            self.changed_entry1(self.entry2)
        else:
            self.inicializaçao = False

    # Método para extrair os fatores de multiplicação de cada unidade da tabela de conversão
    def set_fatores(self):
        self.fator1 = self.config.get_fator(self.unidade1, self.tab)
        self.fator2 = self.config.get_fator(self.unidade2, self.tab)
 
    # Método para conversão
    def changed_entry1(self, widget):    
        # Quando a entry1 é selecionada e alterada:        
        if self.flag_changing_entry1:    
            flag_virgula = False       
            
            # Extrai-se o conteúdo digitado
            value_entry1 = self.entry1.get_text()        
            # Verifica-se se o usuário digitou vírgula 
            flag_virgula = True if "," in value_entry1 else False

            # Transforma-se a string em tipo int ou tipo float
            value_entry1 = parsing_int_float(value_entry1)    
            
            # Se o conteúdo digitado não é um número, chama-se uma flag de erro 
            if value_entry1 == 'Erro':
                # Nada a mostrar na entry2
                self.entry2.set_text('')  
                return None

            # Se a medida usa apenas fator de multiplicação:
            if not self.HasFunction:
                # Atualiza-se os fatores das unidades escolhidas em cada combo box
                self.set_fatores()
                # Realiza-se a conversão
                value_output2 = (self.fator2/self.fator1)*value_entry1
            # Se a medida usa função para cálculo:
            else:
                # Calcula-se a conversão pela função lambda definida com base na unidade de entrada e de saída
                func = self.config.get_function(self.unidade1, self.unidade2, self.tab)                
                try:                
                    # Transforma-se a saída da função de np.array para float
                    value_output2 = float(func(value_entry1))
                except TypeError:
                    # Caso tenha-se conversão de uma mesma unidade (Ex: Celsius = Celsius)
                    value_output2 = value_entry1

            # Arrendoda-se para 3 casas decimais
            value_output2 = round(value_output2, 3)        
            # Retorna na entry2 o resultado da conversão    
            self.entry2.set_text(casting_str(value_output2, flag_virgula))        
                          
    # Método similar a changed_entry1 par modificação na entry2
    def changed_entry2(self, widget):        
        if not self.flag_changing_entry1:
            flag_virgula = False

            value_entry2 = self.entry2.get_text()        
            flag_virgula = True if "," in value_entry2 else False

            value_entry2 = parsing_int_float(value_entry2)

            if value_entry2 == 'Erro':
                self.entry1.set_text('')  
                return None

            if not self.HasFunction:
                self.set_fatores()
                value_output1 = (self.fator1/self.fator2)*value_entry2
            else:
                func = self.config.get_function(self.unidade2, self.unidade1, self.tab)
                try:                
                    value_output1 = float(func(value_entry2))
                except TypeError:
                    value_output1 = value_entry2
                
            value_output1 = round(value_output1, 3)            
            self.entry1.set_text(casting_str(value_output1, flag_virgula))               

    # Método para identificar a seleção da entry  
    def focus_entry1(self, widget):      
        self.flag_changing_entry1 = True
    
    def focus_entry2(self, widget):
        self.flag_changing_entry1 = False 

class Help_Window(Gtk.Window):
    def __init__(self):        
        self.builder = Gtk.Builder()        
        self.builder.add_from_file('help_window.glade')         # Glade XML
        
        self.help_window = self.builder.get_object('help_window') 

        self.builder.connect_signals(self)
        self.help_window.show_all()      

    def delete_help_window(self, widget):        
        Gtk.main_quit()

class Add_Medida_Window(Gtk.Window):
    def __init__(self):        
        self.builder = Gtk.Builder()        
        self.builder.add_from_file('add_medida_window.glade')         # Glade XML
        self.config = TabelasConversao(CONFIG_FILE)

        self.add_medida_window = self.builder.get_object('window_add_medida') 
        self.entry_add_medida = self.builder.get_object('entry_add_medida') 
        self.botao_adicionar = self.builder.get_object('botao_adicionar_medida') 
        self.label_msg = self.builder.get_object('label_msg') 

        self.builder.connect_signals(self)
        self.add_medida_window.show_all()      

    def adicionar_medida(self, widget):
        new_medida = self.entry_add_medida.get_text()
        msg = self.config.add_medida(new_medida)
        self.label_msg.set_text(msg)
      
    def delete_add_medida_window(self, widget):
        Gtk.main_quit()

class Remover_Medida_Window(Gtk.Window):
    def __init__(self):        
        self.builder = Gtk.Builder()        
        self.builder.add_from_file('remover_medida_window.glade')         # Glade XML
        self.config = TabelasConversao(CONFIG_FILE)

        self.remover_medida_window = self.builder.get_object('window_remover_medida') 
        self.combo_medidas = self.builder.get_object('combo_medidas') 
        self.botao_remover = self.builder.get_object('botao_remover_medida')  

        self.tipos_de_medidas = Gtk.ListStore(str) 
         
        for medidas in self.config.get_medidas():  
            self.tipos_de_medidas.append([medidas])  

        self.builder.connect_signals(self)
        self.remover_medida_window.show_all()      

        self.combo_config(self.combo_medidas, self.tipos_de_medidas, 0) 

    def combo_config(self, combo, liststore, i): 
        combo.clear()
        combo.set_model(liststore)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)          
        combo.add_attribute(renderer_text, "text", i)         
        combo.set_active(0)   

    def remover_medida(self, widget):
        model = self.combo_medidas.get_model()
        active = self.combo_medidas.get_active()

        if active >= 0:            
            medida = model[active][0]      
            self.config.remover_medida(medida)
            self.remover_medida_window.close()

    def delete_remover_medida_window(self, widget):
        Gtk.main_quit()

class Add_Unidade_Window(Gtk.Window):
    def __init__(self):        
        self.builder = Gtk.Builder()        
        self.builder.add_from_file('add_unidade_window.glade')         # Glade XML
        self.config = TabelasConversao(CONFIG_FILE)

        self.add_unidade_window1 = self.builder.get_object('window_add_unidade1') 
        self.add_unidade_fator_window = self.builder.get_object('window_add_fator') 
        self.add_unidade_func_window = self.builder.get_object('window_add_func') 

        # Primeira Janela
        self.check_fator = self.builder.get_object('check_fator') 
        self.check_func = self.builder.get_object('check_func') 
        self.combo_medidas = self.builder.get_object('combo_medidas') 
        
        self.tipos_de_medidas = Gtk.ListStore(str) 
         
        for medidas in self.config.get_medidas():  
            self.tipos_de_medidas.append([medidas])

        self.combo_config(self.combo_medidas, self.tipos_de_medidas, 0) 
       
        # Janela Fator       
        self.entry_add_unidade = self.builder.get_object('entry_add_unidade') 
        self.entry_add_fator = self.builder.get_object('entry_add_fator') 
        self.botao_adicionar_unidade1 = self.builder.get_object('botao_adicionar_unidade1') 
        self.label_msg1 = self.builder.get_object('label_msg1') 
        
        # Janela Função
        self.entry_add_unidade_entrada = self.builder.get_object('entry_add_unidade_entrada') 
        self.entry_add_unidade_saída = self.builder.get_object('entry_add_unidade_saída') 
        self.entry_add_func = self.builder.get_object('entry_add_func') 
        self.botao_adicionar_unidade2 = self.builder.get_object('botao_adicionar_unidade2') 
        self.label_msg2 = self.builder.get_object('label_msg2') 

        self.builder.connect_signals(self)
        self.add_unidade_window1.show_all()      
        self.flag_fator = False

    def combo_config(self, combo, liststore, i): 
            combo.clear()
            combo.set_model(liststore)
            renderer_text = Gtk.CellRendererText()
            combo.pack_start(renderer_text, True)          
            combo.add_attribute(renderer_text, "text", i)         
            combo.set_active(0)   

    def focus_fator(self,widget):
        self.flag_fator = True
        if self.check_func.get_active(): self.check_func.set_active(False)    

    def focus_func(self,widget):
        self.flag_fator = False  
        if self.check_fator.get_active(): self.check_fator.set_active(False)

    def open_new_window(self,widget):
        self.medida = self.get_combo_medida()        
        self.add_unidade_window1.hide()

        if self.flag_fator:
            self.add_unidade_fator_window.show_all()            

        else:
            self.add_unidade_func_window.show_all()  

    def get_combo_medida(self):
        model = self.combo_medidas.get_model()
        active = self.combo_medidas.get_active()

        if active >= 0:            
            return model[active][0]    

    def clicked_botao_adicionar_unidade1(self, widget):
        nome_unidade = self.entry_add_unidade.get_text()
        fator_unidade = self.entry_add_fator.get_text()
        
        fator_unidade = parsing_int_float(fator_unidade)

        if fator_unidade == 'Erro':
            self.add_unidade_fator_window.close()
        else:
            msg = self.config.add_unidade_fator(self.medida, nome_unidade, fator_unidade)            
            self.label_msg1.set_text(msg)            

    def clicked_botao_adicionar_unidade2(self, widget):        
        unidade_in = self.entry_add_unidade_entrada.get_text()
        unidade_out = self.entry_add_unidade_saída.get_text()
        func = self.entry_add_func.get_text()

        msg = self.config.add_unidade_func(self.medida, unidade_in, unidade_out, func)
        self.label_msg2.set_text(msg)

    def delete_unidade_window(self, widget):
        Gtk.main_quit()
   

if __name__ == '__main__':
    # Programa principal
    try:
        gui = Main_App_Window()
        Gtk.main()
    except KeyboardInterrupt:
        pass