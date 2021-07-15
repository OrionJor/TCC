from Bases_base import *
from Get_m import *
from In_solution import *


def FeasibilityCheckData(infeasibility_count, infeasibility_string):

    i = 0 # é inteiro
    j = 0 # é inteiro
    #duration_multiplier é tipo Double
    origin_base_id = 0 # é inteiro
    return_base_id = 0 # é intiro
    #reachable é Boolean
    #incompatible_location é Boolean

    #GetVertexData()
    #GetArcData()
    #vehicle_type_list = Vehicle_Type_List_Data()
    #GetVehicleTypeData()
    #GetInstanceData()

    if instance.multi_trip == True:
        num_stops = vertex_list.num_customers
    else:
        num_stops = 1

    infeasibility_count = 0 # é inteiro
    infeasibility_string = "" # é null string

    #perguntar
    #Range(ThisWorkbook.Worksheets(dict("4.Solution")).Cells(vertex_list.num_customers + 8 + num_stops, 1), ThisWorkbook.Worksheets(dict("4.Solution")).Cells(vertex_list.num_customers + 7 + num_stops + (4 * vertex_list.num_customers), 1)).Clear

    max_vehicle_capacity = 0
    total_vehicle_capacity = 0

    for i in range(0, vehicle_type_list.num_vehicle_types):
        if max_vehicle_capacity < vehicle_type_list.vehicle_types[i].capacity:
            max_vehicle_capacity = vehicle_type_list.vehicle_types[i].capacity
        total_vehicle_capacity = total_vehicle_capacity + (vehicle_type_list.vehicle_types[i].NumberAvailable * vehicle_type_list.vehicle_types[i].capacity)

    total_supply = 0
    for i in range(vertex_list.num_depots, vertex_list.num_locations):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].PickupAmount


    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."
        #(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        #print("4.Solution -> planinha 4. Solução", "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória.")

    if (instance.multi_trip == True) and (total_supply > vertex_list.num_customers * total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória."
        #(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
        #print("4.Solution -> planinha 4. Solução", "A capacidade da frota fornecida não é suficiente para transportar a picape obrigatória.")


    total_supply = 0
    # original i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_locations):
        if (vertex_list.vertices[i].mandatory == 1 and vertex_list.vertices[i].PickupAmount < 0) or (vertex_list.vertices[i].PickupAmount > 0):
            total_supply = total_supply + vertex_list.vertices[i].PickupAmount

    if total_supply < 0:
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."
        #print("4.Solution -> planinha 4. Solução", "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta.")
        #(vertex_list.num_customers + 7 + num_stops + infeasibility_count)

    total_supply = 0
    for i in range(vertex_list.num_depots, vertex_list.num_locations):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].DeliveryAmount

    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória."
        #print("4.Solution -> planinha 4. Solução", "A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória.")
        #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
    
    if (instance.multi_trip == True) and (total_supply > vertex_list.num_customers * total_vehicle_capacity + epsilon):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = "A capacidade da frota fornecida não é suficiente para transportar a entrega obrigatória."
        #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)

    for i in range(vertex_list.num_depots, vertex_list.num_locations):
        if ((vertex_list.vertices[i].mandatory == 1) and (-1 *(vertex_list.vertices[i].PickupAmount)) > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A oferta de localização " + " é muito grande para caber em qualquer veículo." + str(i - 1)

            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
            #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count)
            #print("A oferta de localização é muito grande para caber em qualquer veículo.", i - 1)

        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].DeliveryAmount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A demanda de localização " + "é muito grande para caber em qualquer veículo."+ str(i - 1)

            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

            #print("4.Solution", "A demanda de localização" + "é muito grande para caber em qualquer veículo.", i - 1)

        
        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].DeliveryAmount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A demanda de localização " + " é muito grande para caber em qualquer veículo." + str(i - 1) 
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
            #print("4.Solution", "O tempo de serviço da localização", "é mais curto do que sua janela de tempo", i - 1)

    
        if vertex_list.vertices[0].TimeWindowsStart > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "O horário de início da janela de tempo " + " é inválido." + str(i - 1)

            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string +  "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #print("4.Solution", "O horário de início da janela de tempo", " é inválido.", i - 1)
            #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
        

        if vertex_list.vertices[i].TimeWindowsEnd > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "O horário de término da janela de tempo do local," +"é inválido." + str(i - 1)
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #print("4.Solution", "O horário de término da janela de tempo do local", "é invalido")
    
            #print(vertex_list.num_customers, 7, num_stops infeasibility_count, 1)

         
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_locations):
        if instance.open_vrp == False:

            reachable = False
            #For j = 1 To vehicle_type_list.num_vehicle_types
            for j  in range(0, vehicle_type_list.num_vehicle_types):

                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].ReturnBaseId
            
                #if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (arc_list.distance[origin_base_id, i] + arc_list.distance[i, return_base_id] < vehicle_type_list.vehicle_types[j].DistanceLimit):
                #   reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string  + "Localização" + " não pode ser visitado com o limite de distância fornecido." + str(i -1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                #print("4.Solution", i-1, "não pode ser visitado com o limite de distância fornecido.")

                #(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                
            reachable = False
            #j = 1 To vehicle_type_list.num_vehicle_types
            
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].ReturnBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
            
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "não pode ser visitado com o limite de tempo de condução fornecido," + "Localização" + str(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções." + str(i - 1)
                
                #print(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                # dict("Localização ") + 
               

            for j in range(0,vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].ReturnBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
            
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] + duration_multiplier * arc_list.duration[i, return_base_id] + vertex_list.vertices[i].ServiceTime < vehicle_type_list.vehicle_types[j].WorkingTimeLimit):
                   reachable = True

            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não pode ser servido com o limite de tempo de trabalho fornecido." + str(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
        else:
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types anterior
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (arc_list.distance[origin_base_id, i] < vehicle_type_list.vehicle_types[j].DistanceLimit):
                    reachable = True

            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não pode ser visitado com o limite de distância fornecido."+ str(i - 1)

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
                #vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print("4.Solution -> Localização ", i - 1, " não pode ser visitado com o limite de distância fornecido.")  

            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
            
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration[origin_base_id, i] < vehicle_type_list.vehicle_types[j].DrivingTimeLimit):
                    reachable = True

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + str(i - 1) + " não pode ser visitado com o limite de tempo de condução fornecido."
            
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
                #(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
                print("4.Solution -> Localização", i - 1, "não pode ser visitado com o limite de tempo de condução fornecido.")

            reachable = False
            #For j = 1 To vehicle_type_list.num_vehicle_types
            for j in range (0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) + duration_multiplier * vertex_list.vertices[i].ServiceTime < vehicle_type_list.vehicle_types[j].WorkingTimeLimit):
                    reachable = True
            

            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + str(i - 1)  + "não pode ser servido com o limite de tempo de trabalho fornecido."
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização ", i - 1, "não pode ser servido com o limite de tempo de trabalho fornecido.")
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
    

    if instance.backhauls == True:
        #For i = vertex_list.num_depots + 1 To vertex_list.num_locations
        for i in range(vertex_list.num_depots, vertex_list.num_locations):
            if ((-1 * (vertex_list.vertices[i].PickupAmount)) > 0) and (vertex_list.vertices[i].DeliveryAmount > 0):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " +  str(i - 1) + " está pedindo coleta e entrega, o que conflita com a opção de backhauls."
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

                #(dict().Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict
                print("4.Solution", "Location ", i - 1, " está pedindo coleta e entrega, o que conflita com a opção de backhauls.")
    
    
    if instance.vehicle_location_incompatibility == True:
    
        #For i = vertex_list.num_depots + 1 To vertex_list.num_locations
        for i in range(vertex_list.num_depots, vertex_list.num_locations):
            incompatible_location = True
            
            #For j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                if vehicle_type_list.compatible[i, j] == True:
                    incompatible_location = False


            if incompatible_location == True:
            
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização "  +  str(i - 1) + "não é compatível com nenhum tipo de veículo."

                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                print("4.Solution", "Localização ", i - 1, "não é compatível com nenhum tipo de veículo.")




def FeasibilityCheckDataandSolution():

    Compat_vehicle = load_workbook(filename="Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm", read_only=True)   # open an Excel file and return a workbook
    
    if '1. Locais' in Compat_vehicle.sheetnames and '2. Distâncias' in Compat_vehicle.sheetnames and '3. Veiculos' in Compat_vehicle.sheetnames and '4. Solução' in Compat_vehicle.sheetnames:
        print("beleza, tudo OK")
    else:
        print("Planilhas 1.Locais, 2.Distâncias, 3.Veículos e 4. A solução deve existir para a verificação de inviabilidade." + "VRP Spreadsheet Solver")


    GetInstanceData()
    GetVertexData()
    GetArcData()
    GetVehicleTypeData()
    
    dados = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="4. Solução")

    if instance.multi_trip == True:
        num_stops = vertex_list.num_customers
    else:
        num_stops = 1

    #perguntar
    #Range(Cells(2, 1), Cells(2, 16)).Clear
    #Range(Cells(vertex_list.num_customers + 8 + num_stops, 1), Cells(vertex_list.num_customers + 7 + num_stops + (8 * vertex_list.num_customers), 1)).Clear

    infeasibility_count = 0
    infeasibility_string = ""
   

    origin_base_id = 0
    return_base_id = 0

    offset = 0
    stop_count = 0

    #For i = 1 To vehicle_type_list.num_vehicle_types
    #For j = 1 To vehicle_type_list.vehicle_types(i).number_available

    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.num_vehicle_types[i].number_available):

        
            stop_count = (dados.iloc[1,6 + offset])

            #For k = 1 To stop_count
            for k in range(stop_count):
                #If Cells(5 + k, 2 + offset).value = vbNullString
                if (dados.iloc[4+k, 1 + offset]) == "": # De onde foi retirado https://pythonexamples.org/python-check-if-string-is-empty/
                    infeasibility_count = infeasibility_count +1
                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Os locais devem ser contíguos nas rotas. Violação em: " +  str(dados.iloc[4+k, 1 + offset])
                    if infeasibility_count == 5:
                        infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

                    #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
                    print("Os locais devem ser contíguos nas rotas. Violação em:", dados.iloc[4+k, 1 + offset] ) 

                if (k < stop_count) and (dados.iloc[4+k, 1 + offset] == dados.iloc[4, 1 + offset]) and (instance.multi_trip == False):
                    infeasibility_count = infeasibility_count + 1
                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Pode haver no máximo um retorno ao local de partida. Violação em: " + dados.iloc[4+k, 1 + offset] 
                        
                    if infeasibility_count == 5:
                        infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                    
                    ##Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                    print("Pode haver no máximo um retorno ao local de partida. Violação em:" , dados.iloc[4+k, 1 + offset])
                
                if (instance.open_vrp == False) and (k == stop_count) and (dados.iloc[4+k, 1 + offset] + 1 != vehicle_type_list.vehicle_types[i].return_base_id):
                    infeasibility_count = infeasibility_count + 1

                    if infeasibility_count < 5:
                        infeasibility_string = infeasibility_string + "Cada veículo deve retornar ao seu depósito de retorno. Violação em: " + str(dados.iloc[4+k, 1 + offset])
                        #Cells(5 + k, 2 + offset).address
                    if infeasibility_count == 5:
                        infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                        
                    print("Cada veículo deve retornar ao seu depósito de retorno. Violação em:", dados.iloc[4+k, 1 + offset], str(False), str(False))
                    #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value  
                    #Cells(5 + k, 2 + offset).address(False, False) # o que é isso
            
            offset = offset + offset_constant #resolver o deslocamento de tabela para tabela

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

        total_vehicle_capacity = total_vehicle_capacity + (vehicle_type_list.vehicle_types[i].NumberAvailable * vehicle_type_list.vehicle_types[i].capacity)
    
    total_supply = 0
    #vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].PickupAmount

    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."
        print("A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório.")
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
    
    if (instance.multi_trip == True) and (total_supply > total_vehicle_capacity * vertex_list.num_customers):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
        print("A capacidade da frota fornecida não é suficiente para transportar o abastecimento obrigatório.")


    total_supply = 0
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if (vertex_list.vertices[i].mandatory == 1 and vertex_list.vertices[i].PickupAmount < 0) or (vertex_list.vertices[i].PickupAmount > 0):
            total_supply = total_supply + vertex_list.vertices[i].PickupAmount
    
    if total_supply < 0:
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
        print("4.Solution", "Não há suprimento suficiente para itens de coleta para satisfazer a demanda por itens de coleta.")
    
    total_supply = 0
    #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if vertex_list.vertices[i].mandatory == 1:
            total_supply = total_supply + vertex_list.vertices[i].DeliveryAmount


    if (instance.multi_trip == False) and (total_supply > total_vehicle_capacity):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória."
        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
        print("A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória")
    
    if (instance.multi_trip == True) and (total_supply > total_vehicle_capacity * vertex_list.num_customers):
        infeasibility_count = infeasibility_count + 1
        infeasibility_string = infeasibility_string + "A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória"
        ##Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
        print("A capacidade da frota fornecida não é suficiente para transportar a demanda obrigatória")
    
        #i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if (vertex_list.vertices[i].mandatory == 1) and (-1*(vertex_list.vertices[i].PickupAmount) > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "A oferta de localização" + "é muito grande para caber em qualquer veículo."+ str(i - 1)
            
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string  + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("A oferta de Localização", i - 1 ,"é muito grande para caber em qualquer veículo.")
        
        
        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].DeliveryAmount > max_vehicle_capacity):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "A demanda de localização " + "é muito grande para caber em qualquer veículo."+ str(i - 1)
            
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
            
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("A demanda de localização ",  i - 1, "é muito grande para caber em qualquer veículo.")
        

        if (vertex_list.vertices[i].mandatory == 1) and (vertex_list.vertices[i].TimeWindowsEnd - vertex_list.vertices[i].TimeWindowsStart < vertex_list.vertices[i].ServiceTime) :
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5 :
                infeasibility_string = infeasibility_string + "O tempo de serviço da localização" + "é mais curto do que sua janela de tempo." + str(i - 1)
 
            if infeasibility_count == 5 :
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
 
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("O tempo de serviço da Localização ", i - 1, "é mais curto do que sua janela de tempo.")
 
        
        if vertex_list.vertices[i].TimeWindowsStart > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "A janela de tempo, hora de início do local" + " é invalido." + str(i - 1 )
 
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."

            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("A demanda de localização", i - 1, " é inválido.")
        
        if vertex_list.vertices[i].TimeWindowsEnd > 1440:
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string  + "O horário de término da janela de tempo do local " + " é invalido." + str(i - 1)
            
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
        
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("O tempo de término da janela de tempo do Localização", i - 1 , " é inválido.")
    
    #Next i
    #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
        if instance.open_vrp == False:
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
            
                if ((vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (arc_list.distance[origin_base_id, i]) + arc_list.distance[i, return_base_id] < vehicle_type_list.vehicle_types[j].DistanceLimit):
                    reachable = True
        
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " +  "não pode ser visitado com o limite de distância fornecido.." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution" , "Localização ", " não pode ser visitado com o limite de distância fornecido..", i - 1)
            
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
            
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) + duration_multiplier * arc_list.duration[i, return_base_id] < vehicle_type_list.vehicle_types[j].DrivingTimeLimit):
                    reachable = True
                

                
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " +  "não pode ser visitado com o limite de tempo de condução fornecido." + str( i - 1 )
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                print("4.Solution -> Localização ", i - 1, " não pode ser visitado com o limite de tempo de condução fornecido.")
            
    
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[j].return_base_id
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
            
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) + duration_multiplier * arc_list.duration[i, return_base_id] + vertex_list.vertices[i].ServiceTime < vehicle_type_list.vehicle_types[j].WorkingTimeLimit):
                    reachable = True
            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + "não pode ser servido com o limite de tempo de trabalho fornecido. " + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização", i - 1, "não pode ser servido com o limite de tempo de trabalho fornecido.")
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1)
 
        else:
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (arc_list.distance(origin_base_id, i) < vehicle_type_list.vehicle_types[j].DistanceLimit):
                    reachable = True     
                
            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + "não pode ser visitado com o limite de distância fornecido.." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização ", i - 1, " não pode ser visitado com o limite de distância fornecido..") 
                #vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1
                
            
            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) < vehicle_type_list.vehicle_types[j].DrivingTimeLimit):
                    reachable = True
                
                
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não pode ser visitado com o limite de tempo de condução fornecido." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização ", i - 1, " não pode ser visitado com o limite de tempo de condução fornecido.")
            
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
                
    

            reachable = False
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                
                origin_base_id = vehicle_type_list.vehicle_types[j].OriginBaseId
                duration_multiplier = vehicle_type_list.vehicle_types[j].DurationMultiplier
                
                if (vehicle_type_list.vehicle_types[j].NumberAvailable > 0) and (duration_multiplier * arc_list.duration(origin_base_id, i) + vertex_list.vertices[i].ServiceTime < vehicle_type_list.vehicle_types[j].WorkingTimeLimit):
                    reachable = True


            
            if (vertex_list.vertices[i].mandatory == 1) and (reachable == False):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + "não pode ser servido com o limite de tempo de trabalho fornecido." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização" , i - 1, "não pode ser servido com o limite de tempo de trabalho fornecido.")
           
                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
            
        

    if instance.backhauls == True:
        #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
        for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
            if (-1 * (vertex_list.vertices[i].PickupAmount) > 0) and (vertex_list.vertices[i].DeliveryAmount > 0):
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " está pedindo coleta e entrega, o que conflita com a opção de backhauls." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution" , "Localização ", i - 1, " está pedindo coleta e entrega, o que conflita com a opção de backhauls.")

                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
            
       
    if instance.vehicle_Localização_incompatibility == True:
        #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
        for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
            incompatible_Localização = True
            #for j = 1 To vehicle_type_list.num_vehicle_types
            for j in range(0, vehicle_type_list.num_vehicle_types):
                if vehicle_type_list.compatible[i, j] == True:
                    incompatible_Localização = False
                
            
            if incompatible_Localização == True:
            
                infeasibility_count = infeasibility_count + 1
                if infeasibility_count < 5:
                    infeasibility_string = infeasibility_string + "Localização " + " não é compatível com nenhum tipo de veículo." + str(i - 1)
                
                if infeasibility_count == 5:
                    infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
                print("4.Solution", "Localização ", i - 1 , " não é compatível com nenhum tipo de veículo.")

                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = dict
                
    pickup_amount = 0  #é tipo Doube
    delivery_amount = 0 #é tipo Double
    distance_traversed = 0 #é tipo Double
    time_accumulated = 0 #é inteiro
    driving_time_total = 0 #é inteiro
    working_time_total = 0 #é inteiro
    
    total_pickup_load = 0  #é tipo Double
    vehicle_capacity = 0 #é tipo Double
    min_residual_capacity = 0 #é tipo Double
    
    start_index = 0  #é inteiro
    end_index = 0 #é inteiro
    
    this_vertex = 0 #é inteiro
    previous_vertex = 0 #é inteiro
    stop_count_claimed = 0 #é inteiro
    depot_return_count = 0 #é inteiro
  
    #With incumbent -> Para a solução conhecida
    
    offset = 0

    #for i = 1 To vehicle_type_list.num_vehicle_types    
    for i in range(0, vehicle_type_list.num_vehicle_types):
        #for j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
        for j in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
            
            vehicle_capacity = vehicle_type_list.vehicle_types[i].capacity
                
            if instance.multi_trip == True:
                
                #Leia as paradas
                    
                stop_count_claimed = (dados.iloc[1,6] + offset)
                depot_return_count = 0
                    
                start_index = 0
                #for k = 1 To stop_count_claimed
                for k  in range(0, stop_count_claimed):
                    #ThisWorkbook.Worksheets(dict("4.Solution")).Cells(5 + k, 2 + offset).value = ThisWorkbook.Worksheets(dict("4.Solution")).Cells(5, 2 + offset).value:
                    if dados.iloc[4+k, 1 + offset] == dados.iloc[4, 1 + offset]:
                        DP_list.control[start_index] = k - 1 - depot_return_count
                        start_index = k - depot_return_count
                        depot_return_count = depot_return_count + 1            
            else:
                DP_list.control[0] = incumbent.route_vertex_cnt[i, j]
                
                
            if incumbent.route_vertex_cnt[i, j] > 0:
                   
                distance_traversed = 0
                driving_time_total = 0
                working_time_total = 0
                duration_multiplier = vehicle_type_list.vehicle_types[i].DurationMultiplier
                time_accumulated = vehicle_type_list.vehicle_types[i].WorkStartTime
                origin_base_id = vehicle_type_list.vehicle_types[i].OriginBaseId
                return_base_id = vehicle_type_list.vehicle_types[i].ReturnBaseId
            
                incumbent.net_profit_per_route[i, j] = incumbent.net_profit_per_route[i, j] - vehicle_type_list.vehicle_types[i].FixedCostPerTrip
                    
                end_index = 0
                depot_return_count = 0

                #Aqui parrei
                    
                while True:
                    
                    
                    start_index = end_index + 1
                    end_index = DP_list.control[start_index]

                    delivery_amount = 0
                    #for k = start_index To end_index
                    for k in range(start_index, end_index):
                        delivery_amount = delivery_amount + vertex_list.vertices[incumbent.route_vertices[k, i, j]].DeliveryAmount
                        
                        
                    if delivery_amount > vehicle_type_list.vehicle_types[i].capacity:
                        infeasibility_count = infeasibility_count + 1
                        if infeasibility_count < 5:     #str(dados.iloc[1,1+offset])
                            infeasibility_string = infeasibility_string +"A carga do veículo " +  str(dados.iloc[1,1+offset])  + " excede sua capacidade." + str(end_index)
                            
                        if infeasibility_count == 5:
                            infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                            
                        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
                         
                        print("A carga do veículo ", str(dados.iloc[1,1+offset]) , " excede sua capacidade.")
                        
                        
                    pickup_amount = 0
                    #for k = start_index To end_index
                    for k in range(start_index, end_index):
                        
                        if instance.vehicle_Localização_incompatibility == True:
                            if vehicle_type_list.compatible[incumbent.route_vertices[k, i, j], i] == False:
                                infeasibility_count = infeasibility_count + 1
                                if infeasibility_count < 5:
                                    infeasibility_string = infeasibility_string + "Veículo  "  + str(dados.iloc[1,1+offset]) + " está visitando o Localização incompatível " + str(incumbent.route_vertices[k, i, j] - 1) + "."
                                    
                                if infeasibility_count == 5:
                                    infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                                    
                                #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                                print("Veículo ", dados.iloc[1,1+offset], " está visitando o Localização incompatível ",  incumbent.route_vertices[k, i, j] - 1, ".")
                                
                            
                        
                        pickup_amount = pickup_amount + vertex_list.vertices[incumbent.route_vertices[k, i, j]].PickupAmount
                        delivery_amount = delivery_amount - vertex_list.vertices[incumbent.route_vertices[k, i, j]].DeliveryAmount
                
                        if pickup_amount + delivery_amount > vehicle_type_list.vehicle_types[i].capacity:
                            infeasibility_count = infeasibility_count + 1
                            if infeasibility_count < 5:
                                infeasibility_string = infeasibility_string +"Veículo "+ str(dados.iloc[1,1+offset]) + " excede sua capacidade na parada " + str(k + depot_return_count) + "."
                                
                            if infeasibility_count == 5:
                                infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                                
                            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value
                            print("Veícle ", dados.iloc[1,1+offset] , " excede sua capacidade na parada ", k,  ".")
                            
                            
                        if pickup_amount < 0:
                            infeasibility_count = infeasibility_count + 1
                            if infeasibility_count < 5:
                                infeasibility_string = infeasibility_string + "Veículo" + str(dados.iloc[1,1+offset]) + "tem um valor de retirada negativo na parada" + str(k + depot_return_count) + "."
                                
                            if infeasibility_count == 5:
                                    infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                                
                            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value 
                            print("Veícle ", str(dados.iloc[1,1+offset]) + "tem um valor de retirada negativo na parada",  k, ".")
                            
                            
                        if k == start_index:
                            distance_traversed = distance_traversed + arc_list.distance[origin_base_id, incumbent.route_vertices[k, i, j]]
                            time_accumulated = time_accumulated + arc_list.duration[origin_base_id, incumbent.route_vertices[k, i, j]] * duration_multiplier
                            driving_time_total = driving_time_total + arc_list.duration[origin_base_id, incumbent.route_vertices[k, i, j]] * duration_multiplier
                            working_time_total = working_time_total + arc_list.duration[origin_base_id, incumbent.route_vertices[k, i, j]] * duration_multiplier
                        
                        else:
                            distance_traversed = distance_traversed + arc_list.distance(incumbent.route_vertices(i, j, k - 1), incumbent.route_vertices(i, j, k))
                            time_accumulated = time_accumulated + arc_list.duration[incumbent.route_vertices[k - 1, i,  j], incumbent.route_vertices[ k, i, j]] * duration_multiplier
                            driving_time_total = driving_time_total + arc_list.duration[incumbent.route_vertices[k - 1, i,  j], incumbent.route_vertices[ k, i, j]] * duration_multiplier
                            working_time_total = working_time_total + arc_list.duration[incumbent.route_vertices[k - 1, i,  j], incumbent.route_vertices[ k, i, j]] * duration_multiplier
                            
                            
                        if time_accumulated < vertex_list.vertices[incumbent.route_vertices[k, i, j]].TimeWindowsStart:
                            
                            working_time_total = working_time_total + vertex_list.vertices[incumbent.route_vertices[k, i, j]].TimeWindowsStart - time_accumulated
                            time_accumulated = vertex_list.vertices[incumbent.route_vertices[k, i, j]].TimeWindowsStart
                            
                            
                            
                        time_accumulated = time_accumulated + vertex_list.vertices[incumbent.route_vertices[k, i, j]].service_time
                        working_time_total = working_time_total + vertex_list.vertices[incumbent.route_vertices[k, i, j]].service_time
                            
                        if time_accumulated > vertex_list.vertices[incumbent.route_vertices[k, i, j]].TimeWindowsEnd and instance.soft_time_windows == False:
                            infeasibility_count = infeasibility_count + 1
                            if infeasibility_count < 5:
                                infeasibility_string = infeasibility_string +"O tempo de visita do Localização" + incumbent.route_vertices[k, i, j] - 1 + " já passou da sua janela de tempo."
                                
                            if infeasibility_count == 5:
                                infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                                
                            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value =
                            print("O tempo de visita do Localização ", incumbent.route_vertices[k, i, j] - 1, " já passou da sua janela de tempo.")
                            
                
                        
                    if instance.open_vrp == False:
                            
                        k = incumbent.route_vertices[end_index, i, j]
                            
                        distance_traversed = distance_traversed + arc_list.distance[k, return_base_id]
                        time_accumulated = time_accumulated + arc_list.duration[k, return_base_id] * duration_multiplier
                        driving_time_total = driving_time_total + arc_list.duration[k, return_base_id] * duration_multiplier
                        working_time_total = working_time_total + arc_list.duration[k, return_base_id] * duration_multiplier
                            
                        if (time_accumulated > vertex_list.vertices[return_base_id].TimeWindowsEnd) and instance.soft_time_windows == False:
                            infeasibility_count = infeasibility_count + 1
                            if infeasibility_count < 5:
                                infeasibility_string = infeasibility_string +"Veículo " + str(dados.iloc[1,1+offset]) + " " + str(j) + " retorna ao Localização inicial após sua janela de tempo."
                                
                            if infeasibility_count == 5:
                                infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                                
                            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                            print("Veícle ", str(dados.iloc[1,1+offset]), " ", str(j) , " retorna ao Localização inicial após sua janela de tempo.")
                            
                            
                        if incumbent.route_vertex_cnt[i, j] > end_index:
                            time_accumulated = time_accumulated + vertex_list.vertices[return_base_id].ServiceTime
                            working_time_total = working_time_total + vertex_list.vertices[return_base_id].ServiceTime     
                
                        
                        
                    if distance_traversed > vehicle_type_list.vehicle_types[i].distance_limit:
                        infeasibility_count = infeasibility_count + 1
                        if infeasibility_count < 5:
                            infeasibility_string = infeasibility_string +"Veículo " + str(dados.iloc[1,1+offset]) + " " + str(j) + " excede o limite de distância."
                            
                        if infeasibility_count == 5:
                            infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                            
                        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                        print("Veículo ", (dados.iloc[1,1+offset]) , " excede o limite de distância.")
                        
                            
                    if driving_time_total > vehicle_type_list.vehicle_types[i].DrivingTimeLimit:
                        infeasibility_count = infeasibility_count + 1
                        if infeasibility_count < 5:
                            infeasibility_string = infeasibility_string + "Veículo" + str(dados.iloc[1,1+offset]) + " excede o limite de distância."
                            
                        if infeasibility_count == 5:
                            infeasibility_string = infeasibility_string + "Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                            
                        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                        print("Veículo "  , str(dados.iloc[1,1+offset]) , " excede o limite de distância.")
                        
                
                    if working_time_total > vehicle_type_list.vehicle_types[i].WorkingTimeLimit:
                        infeasibility_count = infeasibility_count + 1
                        if infeasibility_count < 5:
                            infeasibility_string = infeasibility_string +"Veículo"  + str(dados.iloc[1,1+offset]) + " " + str(j) + " excede o limite de tempo de trabalho."
                            
                        if infeasibility_count == 5:
                            infeasibility_string = infeasibility_string + " Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                            
                        #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
                        print("Veículo ",  + str(dados.iloc[1,1+offset]) + " " + str(j) + " excede o limite de tempo de trabalho.")
                        
                    
                    depot_return_count = depot_return_count + 1
                    if end_index != incumbent.route_vertex_cnt[i, j]:
                        break
                    
                
                
            offset = offset + offset_constant
                
    #Verificar vértices e visitas obrigatórios
        
    #for i = vertex_list.num_depots + 1 To vertex_list.num_Localizaçãos
    for i in range(vertex_list.num_depots, vertex_list.num_Localizaçãos):
            
        if (vertex_list.vertices[i].mandatory == 1) and (incumbent.vertices_visited[i] != 1):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "Localização " + str(i - 1) + "deve ter sido visitado uma vez (número atual de visitas: " + str(incumbent.vertices_visited[i]) + ")."
                
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string +"Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("Localização ", i - 1, "deve ter sido visitado uma vez (número atual de visitas: ", incumbent.vertices_visited[i],  ").")
            
            
        if (vertex_list.vertices[i].mandatory == -1) and (incumbent.vertices_visited[i] > 0):
            infeasibility_count = infeasibility_count + 1
            if infeasibility_count < 5:
                infeasibility_string = infeasibility_string + "Localização " + str(i - 1) + " não deve ser visitado."
                
            if infeasibility_count == 5:
                infeasibility_string = infeasibility_string + " Mais informações podem ser encontradas nos motivos de inviabilidade detectados na planilha de soluções."
                
            #Cells(vertex_list.num_customers + 7 + num_stops + infeasibility_count, 1).value = 
            print("Localização ",  i - 1, "não deve ser visitado.")
            
            
       
    if infeasibility_count > 0:
        print("Aviso: A última verificação de inviabilidade encontrou problemas com a solução.")
        infeasibility_string = infeasibility_string + " A solução é inviável."
        print("VRP Spreadsheet Solver")
    else:
        reply = ("A solução é viável.", "VRP Spreadsheet Solver")


i = 0
infeasibility_string = ''
FeasibilityCheckData(i, infeasibility_string)