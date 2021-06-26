#from test import *

#b = 10

from Bases_base import *
from Get_m import *
from In_solution import *
from EvaluateRoute_Single_e_Multi_Trip import *


def FeasibilityCheckData(infeasibility_count, infeasibility_string):

    

    if instance.multi_trip == True:
        num_stops = vertex_list.num_customers
    else:
        num_stops = 1

    infeasibility_count = 0
    infeasibility_string = None

    #perguntar
    #Range(ThisWorkbook.Worksheets(dict("4.Solution")).Cells(vertex_list.num_customers + 8 + num_stops, 1), ThisWorkbook.Worksheets(dict("4.Solution")).Cells(vertex_list.num_customers + 7 + num_stops + (4 * vertex_list.num_customers), 1)).Clear

    max_vehicle_capacity = 0
    total_vehicle_capacity = 0

    for i in range(0, vehicle_type_list.num_vehicle_types):
        if max_vehicle_capacity < vehicle_type_list.vehicle_types[i].capacity:
            max_vehicle_capacity = vehicle_type_list.vehicle_types[i].capacity
        total_vehicle_capacity = total_vehicle_capacity + (vehicle_type_list.vehicle_types[i].number_available * vehicle_type_list.vehicle_types[i].capacity)

    total_supply = 0
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos ):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].pickup_amount


    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."
        print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        print(1)
        print("4.Solution -> planinha 4. Solução")
        print("A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."

    if (instance.multi_trip == True) and (total_supply > vertex_list.num_customers * total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."
        print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        print(1)
        print("4.Solution -> planinha 4. Solução")
        print("A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."


    total_supply = 0
    # original i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if (vertex_list.vertices[i].mandatory == 1 and vertex_list.vertices[i].pickup_amount < 0) or (vertex_list.vertices[i].pickup_amount > 0):
            total_supply = total_supply + vertex_list.vertices[i].pickup_amount

    if total_supply < 0:
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."
        print("4.Solution -> planinha 4. Solução")
        print(1)
        print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        print("Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."

    total_supply = 0
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].delivery_amount

    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória."
        print("4.Solution -> planinha 4. Solução")
        print(1)
        print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        print("A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória."
    
    if (instance.multi_trip == True) and (total_supply > vertex_list.num_customers * total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória."
        print(1)
        print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)

    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if ((vertex_list.vertices[i].mandatory == 1) and (-1 *(vertex_list.vertices[i].pickup_amount)) > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A oferta de localização " + " é muito grande para caber em qualquer veículo."
                print(i - 1)

            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
            print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
            print("A oferta de localização é muito grande para caber em qualquer veículo."
            print(i - 1)

        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].delivery_amount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A demanda de localização " + "é muito grande para caber em qualquer veículo."
                print(i - 1)

            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

            print("4.Solution")
            print("A demanda de localização" + "é muito grande para caber em qualquer veículo."
            print(i - 1)

        
        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].delivery_amount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A demanda de localização " + " é muito grande para caber em qualquer veículo."
                print(i - 1) 
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                print("4.Solution")
                print("O tempo de serviço da localização", "é mais curto do que sua janela de tempo")
                print(i - 1)
            
        if vertex_list.vertices[i].time_window_start > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "O horário de início da janela de tempo " + " é inválido."
                print(i - 1)
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string +  "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            print("4.Solution") 
            #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
            print("O horário de início da janela de tempo" + " é inválido."
            print(i - 1)


        if vertex_list.vertices[i].time_window_end > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "O horário de término da janela de tempo do local," +"é inválido."
                print(i - 1)
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            print("4.Solution")
            #print(vertex_list.num_customers, 7, num_stops infeasibility_count, 1)
            print("O horário de término da janela de tempo do local")
            print("é invalido")
    
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if instance.open_vrp == False:

            reachable = False
            for j  in range(0, vehicle_type_list.num_vehicle_types):

                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
            
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (arc_list.distance[origin_base_id, i] + arc_list.distance[i, return_base_id] < vehicle_type_list.vehicle_types[j].distance_limit):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string  + "Localização" + " não pode ser visitado com o limite de distância fornecido."
                    print(i -1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution")
                #(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print(i-1)
                print("não pode ser visitado com o limite de distância fornecido."

                reachable = False
                #j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].duration_multiplier
            
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] + duration_multiplier * arc_list.duration[i, return_base_id] < vehicle_type_list.vehicle_types[j].driving_time_limit):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "não pode ser visitado com o limite de tempo de condução fornecido," + "Localização"
                    print(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict("Localização ") & 
                print(i - 1)

            for j in range(0,vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].duration_multiplier
            
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] + duration_multiplier * arc_list.duration[i, return_base_id] + vertex_list.vertices[i].service_time < vehicle_type_list.vehicle_types[j].working_time_limit):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não pode ser servido com o limite de tempo de trabalho fornecido."
                    print(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
        else:
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types anterior
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (arc_list.distance[origin_base_id, i] < vehicle_type_list.vehicle_types[j].distance_limit):
                    reachable = True

            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não pode ser visitado com o limite de distância fornecido."
                    print(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
                #vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print("4.Solution -> Localização ")
                print(i - 1)
                print(" não pode ser visitado com o limite de distância fornecido."
            
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
            
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].duration_multiplier
                
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] < vehicle_type_list.vehicle_types[j].driving_time_limit):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização "
                    print(i - 1)
                    print(" não pode ser visitado com o limite de tempo de condução fornecido."
            
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
                #(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print("4.Solution -> Localização")
                print(i - 1)
                print("não pode ser visitado com o limite de tempo de condução fornecido."

    
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j  in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].duration_multiplier
                
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] + duration_multiplier * vertex_list.vertices[i].service_time < vehicle_type_list.vehicle_types[j].working_time_limit):
                    reachable = True
                
            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização" + " não pode ser servido com o limite de tempo de trabalho fornecido."
                    print(i - 1)
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                #vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1
                print("4.Solution" + "Localização ")
                print(i - 1 )
                print(" não pode ser servido com o limite de tempo de trabalho fornecido."


    
    if instance.backhauls == True:
        #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos:
        for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
            if (-1* (vertex_list.vertices[i].pickup_amount) > 0) and (vertex_list.vertices[i].delivery_amount > 0):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização," + "está pedindo coleta e entrega, o que conflita com a opção de backhauls."
                    print(i - 1)

                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

                print("4.Solution -> Localização")
                #vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1
                print(i - 1)
                print(" está pedindo coleta e entrega, o que conflita com a opção de backhauls."
        
    
    if instance.vehicle_Localização_incompatibility == True:
    
        #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
        for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
            incompatible_Localização = True
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                if vehicle_type_list.compatible(i, j) == True:
                    incompatible_Localização = False
            
            
            if incompatible_Localização == True:
            
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string  + "Localização " + " não é compatível com nenhum tipo de veículo."
                    print( i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string  + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution")
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print(i - 1)
                print("não é compatível com nenhum tipo de veículo."


def FeasibilityCheckDataandSolution():

    Compat_vehicle = load_workbook(filename="Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm", read_only=True)   # open an Excel file and return a workbook
    
    if '1. Locais' in Compat_vehicle.sheetnames and '2. Distâncias' in Compat_vehicle.sheetnames and '3. Veiculos' in Compat_vehicle.sheetnames and '4. Solução' in Compat_vehicle.sheetnames:
        print("beleza")
    else:
        print("Planilhas 1.Locais, 2.Distâncias, 3.Veículos e 4. A solução deve existir para a verificação de inviabilidade." + "VRP Spreadsheet Solver")


    GetInstanceData()
    GetVertexData()
    GetArcData()
    GetVehicleTypeData()

    if instance.multi_trip == True:
        num_stops = vertex_list.num_customers
    else:
        num_stops = 1

    #perguntar
    #Range(Cells(2, 1), Cells(2, 16)).Clear
    #Range(Cells(vertex_list.num_customers + 8 + num_stops, 1), Cells(vertex_list.num_customers + 7 + num_stops + (8 * vertex_list.num_customers), 1)).Clear

    infeasibility_count = 0

   

    origin_base_id = 0
    return_base_id = 0

    offset = 0
    stop_count = 0

    dados = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="4. Solução")
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.num_vehicle_types[i].number_available):

        
            stop_count = (dados.iloc[1,6] + offset)

            for k in range(stop_count):

                if (dados[4+k, 1 + offset]) == None:
                    infeasibility_count = infeasibility_count +1
                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Os locais devem ser contíguos nas rotas. Violação em:" 
                        #Cells(5 + k, 2 + offset).address
                    if infeasibility_count == 5:
                        infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

                    #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
                    print("Os locais devem ser contíguos nas rotas. Violação em:") 
                    #Cells(5 + k, 2 + offset).address
                if (k < stop_count) and (dados[4+k, 1 + offset] == dados[4, 1 + offset]) and (instance.multi_trip == False):
                    infeasibility_count = infeasibility_count + 1
                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Pode haver no máximo um retorno ao local de partida. Violação em:" 
                        #Cells(5 + k, 2 + offset).address(False, False)
                    if infeasibility_count == 5:
                        infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                    
                    ##Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                    print("Pode haver no máximo um retorno ao local de partida. Violação em:")
                    # Cells(5 + k, 2 + offset).address
                
                if (instance.open_vrp == False) and (k == stop_count) and (dados[4+k, 1 + offset] + 1 != vehicle_type_list.vehicle_types[i].return_base_id):
                    infeasibility_count = infeasibility_count + 1

                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Cada veículo deve retornar ao seu depósito de retorno. Violação em:"
                        #Cells(5 + k, 2 + offset).address
                    if infeasibility_count == 5:
                        print("Cada veículo deve retornar ao seu depósito de retorno. Violação em:")
                        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value  
                        #Cells(5 + k, 2 + offset).address(False, False)
            
            offset = offset + offset_constant

    if infeasibility_count > 0:
        infeasibility_string = "A solução tem problemas de formato:" + infeasibility_string

    incumbent = Solution_Data()

    InitializeSolution(incumbent)
    ReadSolution(incumbent)

    max_vehicle_capacity = 0
    total_vehicle_capacity = 0
    total_supply= 0

    for i in range(0, vehicle_type_list.num_vehicle_types):
        if max_vehicle_capacity < vehicle_type_list.vehicle_types[i].capacity:
            max_vehicle_capacity = vehicle_type_list.vehicle_types[i].capacity

        total_vehicle_capacity = total_vehicle_capacity + (vehicle_type_list.vehicle_types[i].number_available * vehicle_type_list.vehicle_types[i].capacity)
    
    total_supply = 0
    #vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].pickup_amount

    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."
        print("A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
    
    if (instance.multi_trip == True) and (total_supply > total_vehicle_capacity * vertex_list.num_customers):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
        print("A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."


    total_supply = 0
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if (vertex_list.vertices[i].mandatory == 1 and vertex_list.vertices[i].pickup_amount < 0) or (vertex_list.vertices[i].pickup_amount > 0):
            total_supply = total_supply + vertex_list.vertices[i].pickup_amount
    
    if total_supply < 0:
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
        print("4.Solution") 
        print("Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."
    
    total_supply = 0
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].delivery_amount


    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
        # dict("A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória")
    
    if (instance.multi_trip == True) and (total_supply > total_vehicle_capacity * vertex_list.num_customers):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória"
        ##Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
        dict("A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória")
    
        #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if (vertex_list.vertices[i].mandatory == 1) and (-1*(vertex_list.vertices[i].pickup_amount) > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "A oferta de localização" + "é muito grande para caber em qualquer veículo."
                print(i - 1)
            
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string  + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            # dict("The supply of Localização ") & i - 1 & dict("é muito grande para caber em qualquer veículo."
        
        
        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].delivery_amount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "A demanda de localização " + "é muito grande para caber em qualquer veículo."
                print(i - 1)
            
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict("A demanda de localização ") & i - 1 & dict("é muito grande para caber em qualquer veículo."
        

        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].time_window_end - vertex_list.vertices[i].time_window_start < vertex_list.vertices[i].service_time) :
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "O tempo de serviço da localização" + "é mais curto do que sua janela de tempo."
                print(i - 1)
 
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
 
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict("The service time of Localização ") & i - 1 & dict(" is shorter than its time window."
 
        
        if vertex_list.vertices[i].time_window_start > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A janela de tempo, hora de início do local" + " é invalido."
                print(i - 1 )
 
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict(A demanda de localização) & i - 1 & dict(" is invalid."
        
        if vertex_list.vertices[i].time_window_end > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string  + "O horário de término da janela de tempo do local " + " é invalido."
                print(i - 1)
            
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict("The time window end time of Localização ") & i - 1 & dict(" is invalid."
    
    #Next i
    #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if instance.open_vrp == False:
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
            
                if ((vehicle_type_list.vehicle_types[j].number_available > 0) and (arc_list.distance[origin_base_id, i]) + arc_list.distance[i, return_base_id] < vehicle_type_list.vehicle_types[j].distance_limit):
                    reachable = True
        
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " +  "não pode ser visitado com o limite de distância fornecido.."
                    print( i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution" , "Localização ", " não pode ser visitado com o limite de distância fornecido.."
                print(i - 1)
            
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].origin_base_id
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].duration_multiplier
            
                if (vehicle_type_list.vehicle_types[j].number_available > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) + duration_multiplier * arc_list.duration[i, return_base_id] < vehicle_type_list.vehicle_types[j].driving_time_limit):
                    reachable = True
                
                
            
            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " +  "não pode ser visitado com o limite de tempo de condução fornecido."
                    print( i - 1 )
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                print("4.Solution -> Localização ")  
                print(i - 1)
                print(" não pode ser visitado com o limite de tempo de condução fornecido."