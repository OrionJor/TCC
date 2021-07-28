from Bases_base import *
from Improve_Solution2 import *
from AddVertex3_e_Remove3 import *
from Get_m import *


def ImproveSolution(solution, penalty):

    #para saber de qual é a classe
    #solution = Solution_Data()
    #é Long -> é inteiro estendido
    #é Integer -> é inteiro
    iI = 0 # é Long
    jI = 0 # é Long
    kI = 0 #é Long
    
    aI = 0 # é Long
    bI = 0 # é Long
    cI = 0 # é Long

    ip = 0
    jp = 0   
    ap = 0 
    bp = 0

    kp = 0
    
    #vertex = [] # é Long
    vertex = 0
    #vertex_buffer = [] # é  Long
    vertex_buffer = np.zeros((vertex_list.num_customers), dtype ='int16')
    # é Long
    vehicle_type_to_swap2 = 0 # é Long
    vehicle_id_to_swap1 = 0 # é Long
    vehicle_id_to_swap2 = 0 # é Long
    position_to_swap1 = 0 # é Long
    position_to_swap2 = 0 # é Long
    vertex_to_swap = 0 # é Long
    vehicle_id_start_index = 0 # é Long
    
    vehicle_type_to_relocate1 = -1 # é Long
    vehicle_type_to_relocate2 = 0 # é Long
    vehicle_id_to_relocate1 = 0 # é Long
    vehicle_id_to_relocate2 = 0 # é Long
    position_to_relocate1 = 0 # é Long
    position_to_relocate2 = 0 # é Long
    
    vehicle_type_for_2opt1 = -1 # é Long
    vehicle_type_for_2opt2 = 0 # é Long
    vehicle_id_for_2opt1 = 0 # é Long
    vehicle_id_for_2opt2 = 0 # é Long
    position_for_2opt1 = 0 # é Long
    position_for_2opt2 = 0 # é Long
    vertex_cnt_for_2opt1 = 0 # é Long
    vertex_cnt_for_2opt2 = 0 # é Long
    
    reversal_for_2opt1 = 0 # é Long
    reversal_for_2opt2 = 0 # é Long
    
    vehicle_type_for_chain_reversal = -1 # é Long
    vehicle_id_for_chain_reversal = 0 # é Long
    position_for_chain_reversal1 = 0 # é Long
    position_for_chain_reversal2 = 0 # é Long
    midpoint_for_chain_reversal = 0 # é Long
    
    vehicle_type_for_full_swap1 = -1 # é Long
    vehicle_type_for_full_swap2 = 0 # é Long
    vehicle_id_for_full_swap1 = 0 # é Long
    vehicle_id_for_full_swap2 = 0 # é Long
    max_vertex_cnt = 0 # é Long
    vertex_cnt_to_swap = 0 # é Long
    
    max_net_profit = 0 # é Double
    min_total_distance = 0 # é Double
    
    improvement_iterations = 0 # é Integer
    
    #para saber de onde vem os dados
    #GetVertexData()
    #GetVehicleTypeData()
    
    #polishing -> polimento
    
    #MsgBox "Before improvement: " & solution.net_profit '& " " & solution.feasible -> #MsgBox "Antes da melhoria:" & solution.net_profit '& "" & solution.feasible
    max_net_profit = solution.net_profit
    min_total_distance = solution.total_distance
    #swap



    for improvement_iterations in range(0, max_improvement_iterations+1):

        #With solution
        
        max_net_profit = solution.net_profit
        min_total_distance = solution.total_distance
             
        #swap
        
             
        vehicle_type_to_swap1 = -1
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for iI in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
            for jI in range(0, vehicle_type_list.vehicle_types[iI].NumberAvailable):
                #For k = 1 To .route_vertex_cnt[i, j]
                for kI in range(0, solution.route_vertex_cnt[iI, jI]):
                    #For a = i To vehicle_type_list.num_vehicle_types
                    for aI in range(iI, vehicle_type_list.num_vehicle_types):
                        if aI == iI:
                            vehicle_id_start_index = jI
                        else:
                            vehicle_id_start_index = 0

                        #For b = vehicle_id_start_index To vehicle_type_list.vehicle_types[a].NumberAvailable
                        for bI in range(vehicle_id_start_index, vehicle_type_list.vehicle_types[aI].NumberAvailable):
                           #For c = 1 To .route_vertex_cnt[a, b]
                            for cI in range(0, solution.route_vertex_cnt[aI, bI]):
                                vertex_to_swap = solution.route_vertices[kI, iI, jI]
                                solution.route_vertices[kI, iI, jI] = solution.route_vertices[cI, aI, bI]
                                solution.route_vertices[cI, aI, bI] = vertex_to_swap
                                
                                if instance.multi_trip == True :
                                    EvaluateRouteMultiTrip2(solution, iI, jI, penalty)
                                    EvaluateRouteMultiTrip2(solution, aI, bI, penalty)

                                else:
    
                                    EvaluateRouteSingleTrip2(solution, iI, jI, penalty)
                                    EvaluateRouteSingleTrip2(solution, aI, bI, penalty)                             
    
                                if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :

                                    max_net_profit = solution.net_profit
                                    min_total_distance = solution.total_distance
    
                                    vehicle_type_to_swap1 = iI
                                    vehicle_id_to_swap1 = jI
                                    position_to_swap1 = kI
    
                                    vehicle_type_to_swap2 = aI
                                    vehicle_id_to_swap2 = bI
                                    position_to_swap2 = cI
    
                                vertex_to_swap = solution.route_vertices[kI, iI, jI]
                                solution.route_vertices[kI, iI, jI] = solution.route_vertices[cI, aI, bI]
                                solution.route_vertices[cI, aI, bI] = vertex_to_swap
                                
                                if instance.multi_trip == True :
                                    
                                    EvaluateRouteMultiTrip2(solution, iI, jI, penalty)
                                    EvaluateRouteMultiTrip2(solution, aI, bI, penalty)
                                else:
    
                                    EvaluateRouteSingleTrip2(solution, iI, jI, penalty)
                                    EvaluateRouteSingleTrip2(solution, aI, bI, penalty)


                    #print(solution.route_vertices[iI, jI, kI])

                    
        #relocate -> realocar
        vehicle_type_to_relocate1 = -1
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for iI  in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
            for jI  in range(0, vehicle_type_list.vehicle_types[iI].NumberAvailable):
                #For k = 1 To .route_vertex_cnt[i, j]
                for kI  in range(1, solution.route_vertex_cnt[iI, jI]):

                    vertex = solution.route_vertices[kI, iI, jI]
                         
                    RemoveVertex2(solution, iI, jI, kI, penalty)

                    #For a = 1 To vehicle_type_list.num_vehicle_types
                    for aI  in range(0, vehicle_type_list.num_vehicle_types):
                        #For b = 1 To vehicle_type_list.vehicle_types[a].NumberAvailable
                        for bI in range(0, vehicle_type_list.vehicle_types[aI].NumberAvailable):
                            #For c = 1 To .route_vertex_cnt[a, b] + 1
                            for cI  in range(1, solution.route_vertex_cnt[aI, bI]+1):
                                    
                                AddVertex2(solution, vertex, aI, bI, cI, penalty)

                                if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :

                                    max_net_profit = solution.net_profit
                                    min_total_distance = solution.total_distance

                                    vehicle_type_to_relocate1 = iI
                                    vehicle_id_to_relocate1 = jI
                                    position_to_relocate1 = kI

                                    vehicle_type_to_relocate2 = aI
                                    vehicle_id_to_relocate2 = bI
                                    position_to_relocate2 = cI

                                    vehicle_type_to_swap1 = -1
                                    
                                #print(vertex)
                                RemoveVertex2(solution, aI, bI, cI, penalty)

                    AddVertex2(solution, vertex, iI, jI, kI, penalty)

        #'2-opt
        
        vehicle_type_for_2opt1 = -1
             
        #'if (vehicle_type_to_swap1 = -1) And (vehicle_type_to_relocate1 = -1) And (vehicle_type_for_chain_reversal = -1) :
    
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for ip in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
            for jp in range(0, vehicle_type_list.vehicle_types[ip].NumberAvailable):
                        
                #For a = i To vehicle_type_list.num_vehicle_types
                for ap in range(ip, vehicle_type_list.num_vehicle_types):
                        
                    if ap == ip :
                        vehicle_id_start_index = jp + 1
                    else:
                        #vehicle_id_start_index = 1
                        vehicle_id_start_index = 0
                            
                            
                    #For b = vehicle_id_start_index To vehicle_type_list.vehicle_types[a].NumberAvailable
                    for bp in range(vehicle_id_start_index, vehicle_type_list.vehicle_types[ap].NumberAvailable):
                        
                        #If (.route_vertex_cnt(i, j) > 2) And (.route_vertex_cnt(a, b) > 2)
                        if (solution.route_vertex_cnt[ip, jp] > 2) and (solution.route_vertex_cnt[ap, bp] > 2):
                            
                            #For k = 1 To .route_vertex_cnt[i, j] - 1
                            for kp in range(0, solution.route_vertex_cnt[ip, jp] - 1):
                            
                                for cp  in range(0, solution.route_vertex_cnt[ap, bp] - 1):

                                    #anterior
                                    #vertex_cnt_for_2opt1 = (solution.route_vertex_cnt[i, j]) - k
                                    #vertex_cnt_for_2opt2 = (solution.route_vertex_cnt[a, b}) - c
                                    #vertex_cnt_for_2opt1 = (solution.route_vertex_cnt[i, j] -1) - k
                                    #vertex_cnt_for_2opt2 = (solution.route_vertex_cnt[a, b] -1) - c
        
                                    vertex_cnt_for_2opt1 = (solution.route_vertex_cnt[ip, jp]) - (kp + 1)
                                    vertex_cnt_for_2opt2 = (solution.route_vertex_cnt[ap, bp]) - (cp + 1)
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertexp in range(kp + 1, solution.route_vertex_cnt[ip, jp]):
                                        vertex_buffer[vertexp] = solution.route_vertices[vertexp, ip, jp]
                                             
        
                                    #For vertex = c + 1 To .route_vertex_cnt[a, b]
                                    for vertexp in range(cp + 1, solution.route_vertex_cnt[ap, bp]):
                                        solution.route_vertices[kp + vertexp - cp, ip, jp] = solution.route_vertices[vertexp, ap, bp]
                                             
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertexp in range(kp +1 , solution.route_vertex_cnt[ip, jp]):
                                        solution.route_vertices[cp + vertexp - kp, ap, bp] = vertex_buffer[vertexp]
                                             
        
                                    solution.route_vertex_cnt[ip, jp] = (kp + 1 ) + vertex_cnt_for_2opt2
                                    solution.route_vertex_cnt[ap, bp] = (cp + 1 ) + vertex_cnt_for_2opt1

                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                        EvaluateRouteMultiTrip2(solution, ap, bp, penalty)
                                                
                                    else:
        
                                        EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                        EvaluateRouteSingleTrip2(solution, ap, bp, penalty)
                                             
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = ip
                                        vehicle_id_for_2opt1 = jp
                                        position_for_2opt1 = kp
        
                                        vehicle_type_for_2opt2 = ap
                                        vehicle_id_for_2opt2 = bp
                                        position_for_2opt2 = cp
        
                                        reversal_for_2opt1 = 0 # verifica
                                        reversal_for_2opt2 = 0 # verifica
        
                                        vehicle_type_to_swap1 = -1 # verifica
                                        vehicle_type_to_relocate1 = -1 # verifica
                                             
        
                                    #'revert route i,j - > reverter rota i, j
        
                                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[ip, jp] ) - ((kp) + 2)) / 2

                                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5

                                    for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                                        vertex_to_swap = solution.route_vertices[kp + 1 + vertex, ip, jp]
                                        solution.route_vertices[kp + 1 + vertex, ip, jp] = solution.route_vertices[(solution.route_vertex_cnt[ip, jp] -1) - vertex, ip, jp]
                                        solution.route_vertices[(solution.route_vertex_cnt[ip, jp] -1) - vertex, ip, jp] = vertex_to_swap
                                        

                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                                
                                    else:
                                             
                                        EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = ip
                                        vehicle_id_for_2opt1 = jp
                                        position_for_2opt1 = kp
        
                                        vehicle_type_for_2opt2 = ap
                                        vehicle_id_for_2opt2 = bp
                                        position_for_2opt2 = cp
        
                                        reversal_for_2opt1 = 1 # verifica
                                        reversal_for_2opt2 = 0 # verifica
        
                                        vehicle_type_to_swap1 = -1 # verifica
                                        vehicle_type_to_relocate1 = -1 # verifica

                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    #'revert route a,b again
                                    #'revert route a,b -> 'reverter rota a, b
                                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[ap, bp]) - (cp + 2)) / 2
                                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5

                                    for vertex in range(0, int(midpoint_for_chain_reversal) +1):
                                        vertex_to_swap = solution.route_vertices[cp + 1 + vertex, ap, bp]
                                        solution.route_vertices[cp + 1 + vertex, ap, bp] = solution.route_vertices[(solution.route_vertex_cnt[ap, bp] -1) - vertex, ap, bp]
                                        solution.route_vertices[(solution.route_vertex_cnt[ap, bp] -1) - vertex, ap, bp] = vertex_to_swap

                                    
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip2(solution, ap, bp, penalty)
                                                
                                    else:
                                             
                                        EvaluateRouteSingleTrip2(solution, ap, bp, penalty)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = ip
                                        vehicle_id_for_2opt1 = jp
                                        position_for_2opt1 = kp
        
                                        vehicle_type_for_2opt2 = ap
                                        vehicle_id_for_2opt2 = bp
                                        position_for_2opt2 = cp
        
                                        reversal_for_2opt1 = 1 # verifica
                                        reversal_for_2opt2 = 1 # verifica
        
                                        vehicle_type_to_swap1 = -1 # verifica
                                        vehicle_type_to_relocate1 = -1 # verifica
                                             
        
                                    #revert route i,j again -> reverter rota i, j novamente
        
                                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[ip, jp]) - (kp + 2)) / 2
                                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                                        vertex_to_swap = solution.route_vertices[kp + 1 + vertex, ip, jp]
                                        solution.route_vertices[kp + 1 + vertex, ip, jp] = solution.route_vertices[(solution.route_vertex_cnt[ip, jp] -1) - vertex, ip, jp]
                                        solution.route_vertices[(solution.route_vertex_cnt[ip, jp] -1) - vertex, ip, jp] = vertex_to_swap

                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                                
                                    else:
                                                
                                        EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                             
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = ip
                                        vehicle_id_for_2opt1 = jp
                                        position_for_2opt1 = kp
        
                                        vehicle_type_for_2opt2 = ap
                                        vehicle_id_for_2opt2 = bp
                                        position_for_2opt2 = cp
        
                                        reversal_for_2opt1 = 0 # verifica
                                        reversal_for_2opt2 = 1 # verifica
        
                                        vehicle_type_to_swap1 = -1 # verifica
                                        vehicle_type_to_relocate1 = -1 # verifica
                                             
        
                                    #'revert route a,b again
                                    #reverter rota a, b novamente
        
                                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[ap, bp]) - (cp + 2)) / 2
                                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                                        vertex_to_swap = solution.route_vertices[cp + 1 + vertex, ap, bp]
                                        solution.route_vertices[cp + 1 + vertex, ap, bp] = solution.route_vertices[(solution.route_vertex_cnt[ap, bp] -1 ) - vertex, ap, bp]
                                        solution.route_vertices[(solution.route_vertex_cnt[ap, bp] - 1 ) - vertex, ap, bp] = vertex_to_swap
                                        
                                        #solution.route_vertices[c + 1 + vertex, a, b] = solution.route_vertices[(solution.route_vertex_cnt[a, b] -1) - vertex, a, b]
                                        #solution.route_vertices[(solution.route_vertex_cnt[a, b] -1) - vertex, a, b] = vertex_to_swap
                                    
                                    #EvaluateRouteSingleTrip(solution, a, b)
        
                                    vertex_cnt_for_2opt1 = (solution.route_vertex_cnt[ip, jp]) - (kp + 1)
                                    vertex_cnt_for_2opt2 = (solution.route_vertex_cnt[ap, bp]) - (cp + 1)
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(kp + 1, solution.route_vertex_cnt[ip, jp]):
                                        vertex_buffer[vertex] = solution.route_vertices[vertex, ip, jp]
                                             
                                    #For vertex = c + 1 To .route_vertex_cnt[a, b]
                                    for vertex in range(cp + 1, solution.route_vertex_cnt[ap, bp]):
                                        solution.route_vertices[kp + vertex - cp, ip, jp] = solution.route_vertices[vertex, ap, bp]
                                             
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(kp + 1, solution.route_vertex_cnt[ip, jp]):
                                        solution.route_vertices[cp + vertex - kp, ap, bp] = vertex_buffer[vertex]
                                             
        
                                    solution.route_vertex_cnt[ip, jp] = (kp + 1) + vertex_cnt_for_2opt2
                                    solution.route_vertex_cnt[ap, bp] = (cp + 1) + vertex_cnt_for_2opt1
        
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                        EvaluateRouteMultiTrip2(solution, ap, bp, penalty)
                                                
                                    else:
        
                                        EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                        EvaluateRouteSingleTrip2(solution, ap, bp, penalty)

        #chain reversal (2-opt on a single route) -> reversão de cadeia (2 opções em uma única rota)
    
        vehicle_type_for_chain_reversal = -1
    
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
            for j  in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
                #For k = 1 To .route_vertex_cnt[i, j] - 3
                for k  in range(0, solution.route_vertex_cnt[i, j] - 3):
                    #For c = k + 3 To .route_vertex_cnt[i, j]
                    for c in range(k + 3, solution.route_vertex_cnt[i, j]):
    
                        midpoint_for_chain_reversal = (c - k) / 2
                        
                        if ((midpoint_for_chain_reversal - 0.5) >= 1):
                            midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
    
                        
                        #For vertex = 0 To midpoint_for_chain_reversal
                        for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                            vertex_to_swap = solution.route_vertices[k + vertex, i, j]
                            solution.route_vertices[k + vertex, i, j] = solution.route_vertices[c - vertex, i, j]
                            solution.route_vertices[c - vertex, i, j] = vertex_to_swap

                        if instance.multi_trip == True:
                                             
                            EvaluateRouteMultiTrip2(solution, i, j, penalty)
                               
                        else:
                               
                            EvaluateRouteSingleTrip2(solution, i, j, penalty)
                               
                            
    
                        if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)):
                                
                            max_net_profit = solution.net_profit
                            min_total_distance = solution.total_distance
    
                            vehicle_type_for_chain_reversal = i
                            vehicle_id_for_chain_reversal = j
                            position_for_chain_reversal1 = k
                            position_for_chain_reversal2 = c
    
                            vehicle_type_to_swap1 = -1
                            vehicle_type_to_relocate1 = -1
                            vehicle_type_for_2opt1 = -1
                            
    
                        #For vertex = 0 To midpoint_for_chain_reversal
                        for vertex in range(0, int(midpoint_for_chain_reversal) +1):
                            vertex_to_swap = solution.route_vertices[k + vertex, i, j]
                            solution.route_vertices[k + vertex, i, j] = solution.route_vertices[c - vertex, i, j]
                            solution.route_vertices[c - vertex, i, j] = vertex_to_swap
                            
    
                        if instance.multi_trip == True :
                                             
                            EvaluateRouteMultiTrip2(solution, i, j, penalty)
                               
                        else:
                               
                            EvaluateRouteSingleTrip2(solution, i, j, penalty)


        #full swap - exchanging all customers on two vehicles of different types
        #troca total - trocando todos os clientes em dois veículos de tipos diferentes
    
        vehicle_type_for_full_swap1 = -1
    
        if vehicle_type_list.num_vehicle_types > 1 :
             
            #For i = 1 To vehicle_type_list.num_vehicle_types
            for ip in range(0, vehicle_type_list.num_vehicle_types):
                #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
                for jp in range(0, vehicle_type_list.vehicle_types[ip].NumberAvailable):
                    #For a = i + 1 To vehicle_type_list.num_vehicle_types
                    for ap in range(ip + 1, vehicle_type_list.num_vehicle_types):
                        #For b = 1 To vehicle_type_list.vehicle_types[a].NumberAvailable
                        for bp in range(0, vehicle_type_list.vehicle_types[ap].NumberAvailable):
                                  
                            max_vertex_cnt = (solution.route_vertex_cnt[ip, jp])
                                  
                            if max_vertex_cnt < (solution.route_vertex_cnt[ap, bp]):
                                max_vertex_cnt = (solution.route_vertex_cnt[ap, bp])
                                  
                                  
                            #For k = 1 To max_vertex_cnt
                            for k in range(0, max_vertex_cnt):
                                vertex_to_swap = solution.route_vertices[kp, ip, jp]
                                solution.route_vertices[kp, ip, jp] = solution.route_vertices[kp, ap, bp]
                                solution.route_vertices[kp, ap, bp] = vertex_to_swap
            
                                  
                            vertex_cnt_to_swap = solution.route_vertex_cnt[ip, jp]
                            solution.route_vertex_cnt[ip, jp] = solution.route_vertex_cnt[ap, bp]
                            solution.route_vertex_cnt[ap, bp] = vertex_cnt_to_swap
                                  
                            if instance.multi_trip == True :
                                             
                                EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                EvaluateRouteMultiTrip2(solution, ap, bp, penalty)
                                      
                            else:
    
                                EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                EvaluateRouteSingleTrip2(solution, ap, bp, penalty)
                                  

                                  
                            if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                
                                max_net_profit = solution.net_profit
                                min_total_distance = solution.total_distance
            
                                vehicle_type_for_full_swap1 = ip
                                vehicle_id_for_full_swap1 = jp
                                vehicle_type_for_full_swap2 = ap
                                vehicle_id_for_full_swap2 = bp
            
                                vehicle_type_to_swap1 = -1
                                vehicle_type_to_relocate1 = -1
                                vehicle_type_for_2opt1 = -1
                                vehicle_type_for_chain_reversal = -1
                                  
                                  
                            #For k = 1 To max_vertex_cnt
                            for k in range(0, max_vertex_cnt):
                                vertex_to_swap = solution.route_vertices[kp, ip, jp]
                                solution.route_vertices[kp, ip, jp] = solution.route_vertices[kp, ap, bp]
                                solution.route_vertices[kp, ap, bp] = vertex_to_swap
                                  
                            vertex_cnt_to_swap = (solution.route_vertex_cnt[ip, jp])
                            solution.route_vertex_cnt[ip, jp] = solution.route_vertex_cnt[ap, bp]
                            solution.route_vertex_cnt[ap, bp] = vertex_cnt_to_swap
                                  
                            if instance.multi_trip == True :
                                             
                                EvaluateRouteMultiTrip2(solution, ip, jp, penalty)
                                EvaluateRouteMultiTrip2(solution, ap, bp, penalty)
                                      
                            else:
    
                                EvaluateRouteSingleTrip2(solution, ip, jp, penalty)
                                EvaluateRouteSingleTrip2(solution, ap, bp, penalty)

        if vehicle_type_to_swap1 != -1 :
    
            vertex_to_swap = solution.route_vertices[position_to_swap1, vehicle_type_to_swap1, vehicle_id_to_swap1]
            solution.route_vertices[position_to_swap1, vehicle_type_to_swap1, vehicle_id_to_swap1] = solution.route_vertices[position_to_swap2, vehicle_type_to_swap2, vehicle_id_to_swap2]
            solution.route_vertices[position_to_swap2, vehicle_type_to_swap2, vehicle_id_to_swap2] = vertex_to_swap
    
            if instance.multi_trip == True :
                    
                EvaluateRouteMultiTrip2(solution, vehicle_type_to_swap1, vehicle_id_to_swap1, penalty)
                EvaluateRouteMultiTrip2(solution, vehicle_type_to_swap2, vehicle_id_to_swap2, penalty)
                 
            else:
                 
                EvaluateRouteSingleTrip2(solution, vehicle_type_to_swap1, vehicle_id_to_swap1, penalty)
                EvaluateRouteSingleTrip2(solution, vehicle_type_to_swap2, vehicle_id_to_swap2, penalty)
                 
                 
            #print "After swapping: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
            #print "Após a troca:" & solution.net_profit & "" & improvement_iterations' solution.feasible
             
    
            if vehicle_type_to_relocate1 != -1 :
                vertex = solution.route_vertices[position_to_relocate1, vehicle_type_to_relocate1, vehicle_id_to_relocate1]
    
                RemoveVertex2(solution, vehicle_type_to_relocate1, vehicle_id_to_relocate1, position_to_relocate1, penalty)
                AddVertex2(solution, vertex, vehicle_type_to_relocate2, vehicle_id_to_relocate2, position_to_relocate2, penalty)
                 
                #print "After relocating: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                #print "Depois de realocar:" & solution.net_profit & "" & improvement_iterations 'solution.feasible
             
             
            if vehicle_type_for_2opt1 != -1 :
    
                vertex_cnt_for_2opt1 = (solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]) - (position_for_2opt1 + 1)
                vertex_cnt_for_2opt2 = (solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2]) - (position_for_2opt2 + 1)
    
                #For vertex = position_for_2opt1 + 1 To .route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                for vertex in range(position_for_2opt1 +1, solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]):
                    vertex_buffer[vertex] = solution.route_vertices[vertex, vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                
    
                #For vertex = position_for_2opt2 + 1 To .route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2]
                for vertex in range(position_for_2opt2 +1, solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2]):
                    solution.route_vertices[position_for_2opt1 + vertex - position_for_2opt2, vehicle_type_for_2opt1, vehicle_id_for_2opt1] = solution.route_vertices[vertex, vehicle_type_for_2opt2, vehicle_id_for_2opt2]
                
    
                #For vertex = position_for_2opt1 + 1 To .route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                for vertex in range(position_for_2opt1 +1, solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]):
                    solution.route_vertices[position_for_2opt2 + vertex - position_for_2opt1, vehicle_type_for_2opt2, vehicle_id_for_2opt2] = vertex_buffer[vertex]
                
    
                solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1] = (position_for_2opt1 + 1) + vertex_cnt_for_2opt2
                solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2] = (position_for_2opt2 + 1) + vertex_cnt_for_2opt1
    
                if reversal_for_2opt1 == 1 :
    
                    i = vehicle_type_for_2opt1
                    j = vehicle_id_for_2opt1
                    k = position_for_2opt1
    
                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[i, j]) - (k + 2)) / 2
                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
    
                    #For vertex = 0 To midpoint_for_chain_reversal
                    for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                        vertex_to_swap = solution.route_vertices[k + 1 + vertex, i, j]
                        solution.route_vertices[k + 1 + vertex, i, j] = solution.route_vertices[(solution.route_vertex_cnt[i, j] -1) - vertex, i, j]
                        solution.route_vertices[(solution.route_vertex_cnt[i, j] -1) - vertex, i, j] = vertex_to_swap
                    
                
    
                if reversal_for_2opt2 == 1 :
    
                    a = vehicle_type_for_2opt2
                    b = vehicle_id_for_2opt2
                    c = position_for_2opt2
    
                    midpoint_for_chain_reversal = ((solution.route_vertex_cnt[a, b]) - (c + 2)) / 2

                    if ((midpoint_for_chain_reversal - 0.5) >= 1) and (type(midpoint_for_chain_reversal) != float):
                        midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
    
                    #For vertex = 0 To midpoint_for_chain_reversal
                    for vertex in range(0, int(midpoint_for_chain_reversal)+1):
                        vertex_to_swap = solution.route_vertices[c + 1 + vertex, a, b]
                        solution.route_vertices[c + 1 + vertex, a, b] = solution.route_vertices[(solution.route_vertex_cnt[a, b] - 1) - vertex, a, b]
                        solution.route_vertices[(solution.route_vertex_cnt[a, b] -1) - vertex, a, b] = vertex_to_swap
                    
                
    
                if instance.multi_trip == True :
                    
                    EvaluateRouteMultiTrip2(solution, vehicle_type_for_2opt1, vehicle_id_for_2opt1, penalty)
                    EvaluateRouteMultiTrip2(solution, vehicle_type_for_2opt2, vehicle_id_for_2opt2, penalty)
                
                else:
                
                    EvaluateRouteSingleTrip2(solution, vehicle_type_for_2opt1, vehicle_id_for_2opt1, penalty)
                    EvaluateRouteSingleTrip2(solution, vehicle_type_for_2opt2, vehicle_id_for_2opt2, penalty)
    
                
                
                #print "2-opt with reversals: " & reversal_for_2opt1 & " " & reversal_for_2opt2
                #priint "After 2-opt: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                
                #print "2-opt with reversals:" & reversal_for_2opt1 & "" & reversal_for_2opt2
                #print "Após 2 opções:" & solution.net_profit & "" & improvement_iterations' solution.feasible
                 
             
    
            if vehicle_type_for_chain_reversal != -1 :
    
                midpoint_for_chain_reversal = (position_for_chain_reversal2 - position_for_chain_reversal1) / 2
                if ((midpoint_for_chain_reversal - 0.5) >= 1):
                    midpoint_for_chain_reversal = midpoint_for_chain_reversal + 0.5
    
                #For vertex = 0 To midpoint_for_chain_reversal
                for vertex in range(0, int(midpoint_for_chain_reversal) +1):
                    vertex_to_swap = solution.route_vertices[position_for_chain_reversal1 + vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal]
                    solution.route_vertices[position_for_chain_reversal1 + vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal] = solution.route_vertices[position_for_chain_reversal2 - vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal]
                    solution.route_vertices[position_for_chain_reversal2 - vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal] = vertex_to_swap
                
    
                if instance.multi_trip == True :
                
                    EvaluateRouteMultiTrip2(solution, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal, penalty)
                    
                else:
                
                    EvaluateRouteSingleTrip2(solution, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal, penalty)
                
                
    
                #print "After chain reversal: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                #print "Após a reversão da cadeia:" & solution.net_profit & "" & improvement_iterations' solution.feasible
             
             
            if vehicle_type_for_full_swap1 != -1:
    
                max_vertex_cnt = (solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1])
                                  
                if max_vertex_cnt < (solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]):
                    max_vertex_cnt = (solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2])
                
                
                #For vertex = 1 To max_vertex_cnt
                for vertex in range(0, max_vertex_cnt):
                    vertex_to_swap = solution.route_vertices[vertex, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1]
                    solution.route_vertices[vertex, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1] = solution.route_vertices[vertex, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]
                    solution.route_vertices[vertex, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2] = vertex_to_swap
                
                
                vertex_cnt_to_swap = (solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1])
                solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1] = solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]
                solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2] = (vertex_cnt_to_swap)
                
                if instance.multi_trip == True :
                
                    EvaluateRouteMultiTrip2(solution, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1, penalty)
                    EvaluateRouteMultiTrip2(solution, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2, penalty)
                
                else:
                
                    EvaluateRouteSingleTrip2(solution, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1, penalty)
                    EvaluateRouteSingleTrip2(solution, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2, penalty)
    
                
                #print "After full swap: " & solution.net_profit & " " & solution.feasible
                #print "Após a troca completa:" & solution.net_profit & "" & solution.feasible
        
        #if ( ((vehicle_type_to_swap1 != -1) or  (vehicle_type_to_relocate1 != -1) or (vehicle_type_for_2opt1 != -1) or (vehicle_type_for_chain_reversal != -1) or (vehicle_type_for_full_swap1 != -1)) and improvement_iterations > max_improvement_iterations):
            #break

    return solution