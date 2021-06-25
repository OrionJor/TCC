import pandas as pd
from Bases_base2 import *


def Time_Converter(tempo, interval = "secs"):

    hora = tempo.hour
    minutos = tempo.minute
    segundos = tempo.second
    
    '''
    def yrs():
      return divmod(duration_in_s, yr_ct)[0]

    def days():
      return divmod(duration_in_s, day_ct)[0]
    
    def hrs():
      return divmod(duration_in_s, hour_ct)[0]

    '''
    def mins():
        resutado  = (hora*60) + minutos + (segundos /60)
        return resutado
    '''
    def secs(): 
      return duration_in_s
    '''
    return {
        'mins': int(mins())
        #'secs': int(secs())
    }[interval]







def GetVertexData():
    dados = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="VRP Solver Console")

    vertex_list = Vertex_List_Data()

    vertex_list.num_depots = dados.iloc[3, 2]

    vertex_list.num_customers = dados.iloc[4, 2]
    vertex_list.num_locations = vertex_list.num_depots + vertex_list.num_customers
    

    #cria vetor estático
    dados2 = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="1. Locais")
    i = 0
    matriz = []
    t = 'time_windows_start'
    
    #vertex_list.num_locations= 23
    
    dados3 = [] #->linhas
    for i in range(1, vertex_list.num_locations):
        tempo_inicio = dados2.iloc[i,6]
        dados3 += [Time_Converter(tempo_inicio, 'mins')]
        #vertex_list.vertices.time_window_start = [Time_Converter(tempo_inicio, 'mins')]

    for i in range(0,(len(dados3)+1)):
        if i == 0:
          matriz = [t]
        elif i == 1:
          matriz += [dados3[i-1]]
        else:
          matriz += [dados3[i-1]]

    print(matriz)

GetVertexData()