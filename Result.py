from Bases_base import *
import pandas as pd
from xlsxwriter import worksheet

solution = Solution_Data()

solution.net_profit = 10

sheet = 17
offset = 0


#Crie um dataframe do Pandas a partir de alguns dados.
data = [10, None, 30, 40, 50, 60]
df = pd.DataFrame({ 'Parar a contagem':data,
                    'Nome do local': data,
                    'ID de localização' : data,
                    'Latitude (y)' : data,
                    'Longitude (x)':data,
                    'Distância viajada':data,
                    'Tempo de condução':data,
                    'Tempo de chegada':data,
                    'Hora de partida':data,
                    'Expediente':data,
                    'Lucro coletado':data,
                    'Valor de retirada':data,
                    'Quantidade de entrega':data,
                    'Coleta cumulativa':data,
                    'Entrega subtrativa':data,
                    'Carga':data})


# Crie um escritor do Pandas Excel usando XlsxWriter como mecanismo.
writer = pd.ExcelWriter("Resultado.xlsx", engine='xlsxwriter')

for i in range(1, 3):

    if i == 1:

        # Converta o dataframe em um objeto Excel XlsxWriter. Observe que desligamos
        # o cabeçalho padrão e pula uma linha para nos permitir inserir um definido pelo usuário
        # cabeçalho.
        df.to_excel(writer, sheet_name='Sheet1', startrow=4, header=False, index=False)


        # Obtenha a pasta de trabalho xlsxwriter e os objetos de planilha.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']


        # Reescreva os cabeçalhos das colunas sem formatar.
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(3, col_num, value)

        worksheet.write(2, i, "Veículo:")
        worksheet.write(2, i+1, "V1 "+ " Nome Veículo")

        worksheet.write(2, i+5, "Para: ")
        worksheet.write(2, i+6, "numero de vertices")
        worksheet.write(2, i+7, "Lucro líquido total:")
        worksheet.write(2, i+8, "Valor")

        # Adicione um formato à coluna B.
        format1 = workbook.add_format({'font_color': 'red'})

        worksheet.set_column('B:B', 11, format1)

    else:

        # Converta o dataframe em um objeto Excel XlsxWriter. Observe que desligamos
        # o cabeçalho padrão e pula uma linha para nos permitir inserir um definido pelo usuário
        # cabeçalho.
        df.to_excel(writer, sheet_name='Sheet1', startrow=4, header=False, startcol=offset, index=False)


        # Obtenha a pasta de trabalho xlsxwriter e os objetos de planilha.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']


        # Reescreva os cabeçalhos das colunas sem formatar.
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(3, col_num + offset, value)

        worksheet.write(2, offset, "Veículo:")
        worksheet.write(2, offset+1, "V1 "+ " Nome Veículo")

        worksheet.write(2, offset+5, "Para: ")
        worksheet.write(2, offset+6, "numero de vertices")
        worksheet.write(2, offset+7, "Lucro líquido total:")
        worksheet.write(2, offset+8, "Valor")

        # Adicione um formato à coluna B.
        format1 = workbook.add_format({'font_color': 'black'})

        worksheet.set_column('B:B', 11, format1)

    offset = offset + sheet


worksheet.write("A1", 'Lucro líquido total:')
worksheet.write("B1", "Valor")
# Feche o gravador do Pandas Excel e gere o arquivo do Excel.
writer.save()