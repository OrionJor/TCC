import pandas as pd
import warnings
from openpyxl import load_workbook

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
'''
def a():
   global b
   b = "teste"
   b = 10

a()

b = 100
print(b)

def tes():
    
   global a 
   a = 0
   #a = 1
   if a == 0:
      t()
      t()
      t()
   
   print(a)

def t():

   global a 
   a = 0
   a = 2


#tes()

dados = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="4. Solução")

#informações de dados valor de linha -2 e valor de coluna -1
k = 0

offset = 0

#print(dados.iloc[3 + k, 2]) formula

print(dados.iloc[4, 2 + offset])
'''