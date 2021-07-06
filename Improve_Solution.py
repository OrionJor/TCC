from Bases_base import *
from In_solution import *
from Get_m import *
from Flesibility import *
from EvaluateRoute_Single_e_Multi_Trip import *




def ImproveSolution(solution):

    #é Long -> é inteiro estendido
    #é Integer -> é inteiro
    i = 0 # é Long
    j = 0 # é Long
    k = 0 #é Long
    
    a = 0 # é Long
    b = 0 # é Long
    c = 0 # é Long
    
    vertex = None # é Long
    vertex_buffer = [] # é  Long
    vertex_buffer = [[] for i in range(vertex_list.num_customers)]
    
    vehicle_type_to_swap1 = None # é Long
    vehicle_type_to_swap2 = None # é Long
    vehicle_id_to_swap1 = None # é Long
    vehicle_id_to_swap2 = None # é Long
    position_to_swap1 = None # é Long
    position_to_swap2 = None # é Long
    vertex_to_swap = None # é Long
    vehicle_id_start_index = None # é Long
    
    vehicle_type_to_relocate1 = None # é Long
    vehicle_type_to_relocate2 = None # é Long
    vehicle_id_to_relocate1 = None # é Long
    vehicle_id_to_relocate2 = None # é Long
    position_to_relocate1 = None # é Long
    position_to_relocate2 = None # é Long
    
    vehicle_type_for_2opt1 = None # é Long
    vehicle_type_for_2opt2 = None # é Long
    vehicle_id_for_2opt1 = None # é Long
    vehicle_id_for_2opt2 = None # é Long
    position_for_2opt1 = None # é Long
    position_for_2opt2 = None # é Long
    vertex_cnt_for_2opt1 = None # é Long
    vertex_cnt_for_2opt2 = None # é Long
    
    reversal_for_2opt1 = None # é Long
    reversal_for_2opt2 = None # é Long
    
    vehicle_type_for_chain_reversal = None # é Long
    vehicle_id_for_chain_reversal = None # é Long
    position_for_chain_reversal1 = None # é Long
    position_for_chain_reversal2 = None # é Long
    midpoint_for_chain_reversal = None # é Long
    
    vehicle_type_for_full_swap1 = None # é Long
    vehicle_type_for_full_swap2 = None # é Long
    vehicle_id_for_full_swap1 = None # é Long
    vehicle_id_for_full_swap2 = None # é Long
    max_vertex_cnt = None # é Long
    vertex_cnt_to_swap = None # é Long
    
    max_net_profit = None # é Double
    min_total_distance = None # é Double
    
    improvement_iterations = None # é Integer
    
    improvement_iterations = 0
    
    #polishing -> polimento
    
    #MsgBox "Before improvement: " & solution.net_profit '& " " & solution.feasible -> #MsgBox "Antes da melhoria:" & solution.net_profit '& "" & solution.feasible
    
    
    
    while True:

        #With solution
        
        max_net_profit = solution.net_profit
        min_total_distance = solution.total_distance
             
        #swap
             
        vehicle_type_to_swap1 = -1
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].number_available
            for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                #For k = 1 To .route_vertex_cnt[i, j]
                for k in range(0, solution.route_vertex_cnt[i, j]):
                    #For a = i To vehicle_type_list.num_vehicle_types
                    for a in range(i, vehicle_type_list.num_vehicle_types):
                             
                        if a == i:
                            vehicle_id_start_index = j
                        else:
                            vehicle_id_start_index = 1

                        #For b = vehicle_id_start_index To vehicle_type_list.vehicle_types[a].number_available
                        for b in range(vehicle_id_start_index, vehicle_type_list.vehicle_types[a].number_available):
                            #For c = 1 To .route_vertex_cnt[a, b]
                            for c in range(0, solution.route_vertex_cnt[a, b]):
    
                                vertex_to_swap = solution.route_vertices[k, i, j]
                                solution.route_vertices[k, i, j] = solution.route_vertices[c, a, b]
                                solution.route_vertices[c, a, b] = vertex_to_swap
                                    
                                if instance.multi_trip == True :
                                    
                                    EvaluateRouteMultiTrip(solution, i, j)
                                    EvaluateRouteMultiTrip(solution, a, b)

                                else:
    
                                    EvaluateRouteSingleTrip(solution, i, j)
                                    EvaluateRouteSingleTrip(solution, a, b)
                                    
                                    
    
                                if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                        
                                    max_net_profit = solution.net_profit
                                    min_total_distance = solution.total_distance
    
                                    vehicle_type_to_swap1 = i
                                    vehicle_id_to_swap1 = j
                                    position_to_swap1 = k
    
                                    vehicle_type_to_swap2 = a
                                    vehicle_id_to_swap2 = b
                                    position_to_swap2 = c
                                    
    
                                vertex_to_swap = solution.route_vertices[k, i, j]
                                solution.route_vertices[k, i, j] = solution.route_vertices[c, a, b]
                                solution.route_vertices[c, a, b] = vertex_to_swap
                                    
                                if instance.multi_trip == True :
                                    
                                    EvaluateRouteMultiTrip(solution, i, j)
                                    EvaluateRouteMultiTrip(solution, a, b)
                                else:
    
                                    EvaluateRouteSingleTrip(solution, i, j)
                                    EvaluateRouteSingleTrip(solution, a, b)
                                    
    
        #relocate -> realocar

        vehicle_type_to_relocate1 = -1
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i  in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].number_available
            for j  in range(0, vehicle_type_list.vehicle_types[i].number_available):
                #For k = 1 To .route_vertex_cnt[i, j]
                for k  in range(0, solution.route_vertex_cnt[i, j]):

                    vertex = solution.route_vertices[k, i, j]
                         
                    RemoveVertex(solution, i, j, k)

                    #For a = 1 To vehicle_type_list.num_vehicle_types
                    for a  in range(0, vehicle_type_list.num_vehicle_types):
                        #For b = 1 To vehicle_type_list.vehicle_types[a].number_available
                        for b in range(0, vehicle_type_list.vehicle_types[a].number_available):
                            #For c = 1 To .route_vertex_cnt[a, b] + 1
                            for c  in range(0, solution.route_vertex_cnt[a, b] + 1):
                                    
                                AddVertex(solution, vertex, a, b, c)

                                if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :

                                    max_net_profit = solution.net_profit
                                    min_total_distance = solution.total_distance

                                    vehicle_type_to_relocate1 = i
                                    vehicle_id_to_relocate1 = j
                                    position_to_relocate1 = k

                                    vehicle_type_to_relocate2 = a
                                    vehicle_id_to_relocate2 = b
                                    position_to_relocate2 = c

                                    vehicle_type_to_swap1 = -1
                                    

                                RemoveVertex(solution, a, b, c)
           
                    AddVertex(solution, vertex, i, j, k)


        #'2-opt
        
        vehicle_type_for_2opt1 = -1
             
        #'if (vehicle_type_to_swap1 = -1) And (vehicle_type_to_relocate1 = -1) And (vehicle_type_for_chain_reversal = -1) :
    
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].number_available
            for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                        
                #For a = i To vehicle_type_list.num_vehicle_types
                for a in range(i, vehicle_type_list.num_vehicle_types):
                        
                    if a == i :
                        vehicle_id_start_index = j + 1
                    else:
                        vehicle_id_start_index = 1
                            
                            
                    #For b = vehicle_id_start_index To vehicle_type_list.vehicle_types[a].number_available
                    for b in range(vehicle_id_start_index, vehicle_type_list.vehicle_types[a].number_available):
                                
                        if (solution.route_vertex_cnt[i, j] > 2) and (solution.route_vertex_cnt[a, b] > 2) :
                                    
                            #For k = 1 To .route_vertex_cnt[i, j] - 1
                            for k in range(0, solution.route_vertex_cnt[i, j] - 1):
                                #For c = 1 To .route_vertex_cnt[a, b] - 1
                                for c  in range(0, solution.route_vertex_cnt[a, b] - 1):
        
                                    vertex_cnt_for_2opt1 = solution.route_vertex_cnt[i, j] - k
                                    vertex_cnt_for_2opt2 = solution.route_vertex_cnt[a, b] - c
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(k + 1, solution.route_vertex_cnt[i, j]):
                                        vertex_buffer[vertex] = solution.route_vertices[vertex, i, j]
                                             
        
                                    #For vertex = c + 1 To .route_vertex_cnt[a, b]
                                    for vertex in range(c, solution.route_vertex_cnt[a, b]):
                                        solution.route_vertices[k + vertex - c, i, j] = solution.route_vertices[vertex, a, b]
                                             
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(k, solution.route_vertex_cnt[i, j]):
                                        solution.route_vertices[c + vertex - k, a, b] = vertex_buffer[vertex]
                                             
        
                                    solution.route_vertex_cnt[i, j] = k + vertex_cnt_for_2opt2
                                    solution.route_vertex_cnt[a, b] = c + vertex_cnt_for_2opt1
                                             
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip(solution, i, j)
                                        EvaluateRouteMultiTrip(solution, a, b)
                                                
                                    else:
        
                                        EvaluateRouteSingleTrip(solution, i, j)
                                        EvaluateRouteSingleTrip(solution, a, b)
                                             
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = i
                                        vehicle_id_for_2opt1 = j
                                        position_for_2opt1 = k
        
                                        vehicle_type_for_2opt2 = a
                                        vehicle_id_for_2opt2 = b
                                        position_for_2opt2 = c
        
                                        reversal_for_2opt1 = 0
                                        reversal_for_2opt2 = 0
        
                                        vehicle_type_to_swap1 = -1
                                        vehicle_type_to_relocate1 = -1
                                             
        
                                    #'revert route i,j - > reverter rota i, j
        
                                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[i, j] - (k + 1)) / 2
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, midpoint_for_chain_reversal):
                                        vertex_to_swap = solution.route_vertices[k + 1 + vertex, i, j]
                                        solution.route_vertices[k + 1 + vertex, i, j] = solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j]
                                        solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j] = vertex_to_swap
                                             
        
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip(solution, i, j)
                                                
                                    else:
                                             
                                        EvaluateRouteSingleTrip(solution, i, j)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = i
                                        vehicle_id_for_2opt1 = j
                                        position_for_2opt1 = k
        
                                        vehicle_type_for_2opt2 = a
                                        vehicle_id_for_2opt2 = b
                                        position_for_2opt2 = c
        
                                        reversal_for_2opt1 = 1
                                        reversal_for_2opt2 = 0
        
                                        vehicle_type_to_swap1 = -1
                                        vehicle_type_to_relocate1 = -1
                                             
        
                                    #'revert route a,b -> 'reverter rota a, b
        
                                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[a, b] - (c + 1)) / 2
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, midpoint_for_chain_reversal):
                                        vertex_to_swap = solution.route_vertices[c + 1 + vertex, a, b]
                                        solution.route_vertices[c + 1 + vertex, a, b] = solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b]
                                        solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b] = vertex_to_swap
                                             
        
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip(solution, a, b)
                                                
                                    else:
                                             
                                        EvaluateRouteSingleTrip(solution, a, b)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                                 
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = i
                                        vehicle_id_for_2opt1 = j
                                        position_for_2opt1 = k
        
                                        vehicle_type_for_2opt2 = a
                                        vehicle_id_for_2opt2 = b
                                        position_for_2opt2 = c
        
                                        reversal_for_2opt1 = 1
                                        reversal_for_2opt2 = 1
        
                                        vehicle_type_to_swap1 = -1
                                        vehicle_type_to_relocate1 = -1
                                             
        
                                    #revert route i,j again -> reverter rota i, j novamente
        
                                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[i, j] - (k + 1)) / 2
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, midpoint_for_chain_reversal):
                                        vertex_to_swap = solution.route_vertices[k + 1 + vertex, i, j]
                                        solution.route_vertices[k + 1 + vertex, i, j] = solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j]
                                        solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j] = vertex_to_swap
                                             
        
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip(solution, i, j)
                                                
                                    else:
                                                
                                        EvaluateRouteSingleTrip(solution, i, j)
                                                
                                             
        
                                    if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                             
                                        max_net_profit = solution.net_profit
                                        min_total_distance = solution.total_distance
        
                                        vehicle_type_for_2opt1 = i
                                        vehicle_id_for_2opt1 = j
                                        position_for_2opt1 = k
        
                                        vehicle_type_for_2opt2 = a
                                        vehicle_id_for_2opt2 = b
                                        position_for_2opt2 = c
        
                                        reversal_for_2opt1 = 0
                                        reversal_for_2opt2 = 1
        
                                        vehicle_type_to_swap1 = -1
                                        vehicle_type_to_relocate1 = -1
                                             
        
                                    #'revert route a,b again
                                    #reverter rota a, b novamente
        
                                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[a, b] - (c + 1)) / 2
        
                                    #For vertex = 0 To midpoint_for_chain_reversal
                                    for vertex in range(0, midpoint_for_chain_reversal):
                                        vertex_to_swap = solution.route_vertices[c + 1 + vertex, a, b]
                                        solution.route_vertices[c + 1 + vertex, a, b] = solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b]
                                        solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b] = vertex_to_swap
                                             
        
                                    #EvaluateRouteSingleTrip(solution, a, b)
        
                                    vertex_cnt_for_2opt1 = solution.route_vertex_cnt[i, j] - k
                                    vertex_cnt_for_2opt2 = solution.route_vertex_cnt[a, b] - c
        
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(k, solution.route_vertex_cnt[i, j]):
                                        vertex_buffer[vertex] = solution.route_vertices[vertex, i, j]
                                             
                                    #For vertex = c + 1 To .route_vertex_cnt[a, b]
                                    for vertex in range(c, solution.route_vertex_cnt[a, b]):
                                        solution.route_vertices[k + vertex - c, i, j] = solution.route_vertices[vertex, a, b]
                                             
                                    #For vertex = k + 1 To .route_vertex_cnt[i, j]
                                    for vertex in range(k + 1, solution.route_vertex_cnt[i, j]):
                                        solution.route_vertices[c + vertex - k, a, b] = vertex_buffer[vertex]
                                             
        
                                    solution.route_vertex_cnt[i, j] = k + vertex_cnt_for_2opt2
                                    solution.route_vertex_cnt[a, b] = c + vertex_cnt_for_2opt1
        
                                    if instance.multi_trip == True :
                                             
                                        EvaluateRouteMultiTrip(solution, i, j)
                                        EvaluateRouteMultiTrip(solution, a, b)
                                                
                                    else:
        
                                        EvaluateRouteSingleTrip(solution, i, j)
                                        EvaluateRouteSingleTrip(solution, a, b)
            
                                             
             
             

        #chain reversal (2-opt on a single route) -> reversão de cadeia (2 opções em uma única rota)
    
        vehicle_type_for_chain_reversal = -1
    
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types[i].number_available
            for j  in range(0, vehicle_type_list.vehicle_types[i].number_available):
                #For k = 1 To .route_vertex_cnt[i, j] - 3
                for k  in range(0, solution.route_vertex_cnt[i, j] - 3):
                    #For c = k + 3 To .route_vertex_cnt[i, j]
                    for c in range(k + 2, solution.route_vertex_cnt[i, j]):
    
                        midpoint_for_chain_reversal = (c - k) / 2
    
                        #For vertex = 0 To midpoint_for_chain_reversal
                        for vertex in range(0, midpoint_for_chain_reversal):
                            vertex_to_swap = solution.route_vertices[k + vertex, i, j]
                            solution.route_vertices[k + vertex, i, j] = solution.route_vertices[c - vertex, i, j]
                            solution.route_vertices[c - vertex, i, j] = vertex_to_swap
                            
    
                        if instance.multi_trip == True:
                                             
                            EvaluateRouteMultiTrip(solution, i, j)
                               
                        else:
                               
                            EvaluateRouteSingleTrip(solution, i, j)
                               
                            
    
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
                        for vertex in range(0, midpoint_for_chain_reversal):
                            vertex_to_swap = solution.route_vertices[k + vertex, i, j]
                            solution.route_vertices[k + vertex, i, j] = solution.route_vertices[c - vertex, i, j]
                            solution.route_vertices[c - vertex, i, j] = vertex_to_swap
                            
    
                        if instance.multi_trip == True :
                                             
                            EvaluateRouteMultiTrip(solution, i, j)
                               
                        else:
                               
                            EvaluateRouteSingleTrip(solution, i, j)
                               
               
        #full swap - exchanging all customers on two vehicles of different types
        #troca total - trocando todos os clientes em dois veículos de tipos diferentes
    
        vehicle_type_for_full_swap1 = -1
    
        if vehicle_type_list.num_vehicle_types > 1 :
             
            #For i = 1 To vehicle_type_list.num_vehicle_types
            for i in range(0, vehicle_type_list.num_vehicle_types):
                #For j = 1 To vehicle_type_list.vehicle_types[i].number_available
                for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                    #For a = i + 1 To vehicle_type_list.num_vehicle_types
                    for a in range(i, vehicle_type_list.num_vehicle_types):
                        #For b = 1 To vehicle_type_list.vehicle_types[a].number_available
                        for b in range(0, vehicle_type_list.vehicle_types[a].number_available):
                                  
                            max_vertex_cnt = solution.route_vertex_cnt[i, j]
                                  
                            if max_vertex_cnt < solution.route_vertex_cnt[a, b] :
                                max_vertex_cnt = solution.route_vertex_cnt[a, b]
                                  
                                  
                            #For k = 1 To max_vertex_cnt
                            for k in range(0, max_vertex_cnt):
                                vertex_to_swap = solution.route_vertices[k, i, j]
                                solution.route_vertices[k, i, j] = solution.route_vertices[k, a, b]
                                solution.route_vertices[k, a, b] = vertex_to_swap
            
                                  
                            vertex_cnt_to_swap = solution.route_vertex_cnt[i, j]
                            solution.route_vertex_cnt[i, j] = solution.route_vertex_cnt[a, b]
                            solution.route_vertex_cnt[a, b] = vertex_cnt_to_swap
                                  
                            if instance.multi_trip == True :
                                             
                                EvaluateRouteMultiTrip(solution, i, j)
                                EvaluateRouteMultiTrip(solution, a, b)
                                      
                            else:
    
                                EvaluateRouteSingleTrip(solution, i, j)
                                EvaluateRouteSingleTrip(solution, a, b)
                                  
                                  
                                  
                            if (solution.net_profit > max_net_profit + epsilon) or ((solution.net_profit > max_net_profit - epsilon) and (solution.total_distance < min_total_distance - epsilon)) :
                                
                                max_net_profit = solution.net_profit
                                min_total_distance = solution.total_distance
            
                                vehicle_type_for_full_swap1 = i
                                vehicle_id_for_full_swap1 = j
                                vehicle_type_for_full_swap2 = a
                                vehicle_id_for_full_swap2 = b
            
                                vehicle_type_to_swap1 = -1
                                vehicle_type_to_relocate1 = -1
                                vehicle_type_for_2opt1 = -1
                                vehicle_type_for_chain_reversal = -1
                                  
                                  
                            #For k = 1 To max_vertex_cnt
                            for k in range(0, max_vertex_cnt):
                                vertex_to_swap = solution.route_vertices[k, i, j]
                                solution.route_vertices[k, i, j] = solution.route_vertices[k, a, b]
                                solution.route_vertices[k, a, b] = vertex_to_swap
                                  
                                vertex_cnt_to_swap = solution.route_vertex_cnt[i, j]
                                solution.route_vertex_cnt[i, j] = solution.route_vertex_cnt[a, b]
                                solution.route_vertex_cnt[a, b] = vertex_cnt_to_swap
                                  
                            if instance.multi_trip == True :
                                             
                                EvaluateRouteMultiTrip(solution, i, j)
                                EvaluateRouteMultiTrip(solution, a, b)
                                      
                            else:
    
                                EvaluateRouteSingleTrip(solution, i, j)
                                EvaluateRouteSingleTrip(solution, a, b)

             
        if vehicle_type_to_swap1 != -1 :
    
            vertex_to_swap = solution.route_vertices[position_to_swap1, vehicle_type_to_swap1, vehicle_id_to_swap1]
            solution.route_vertices[position_to_swap1, vehicle_type_to_swap1, vehicle_id_to_swap1] = solution.route_vertices[position_to_swap2, vehicle_type_to_swap2, vehicle_id_to_swap2]
            solution.route_vertices[position_to_swap2, vehicle_type_to_swap2, vehicle_id_to_swap2] = vertex_to_swap
    
            if instance.multi_trip == True :
                    
                EvaluateRouteMultiTrip(solution, vehicle_type_to_swap1, vehicle_id_to_swap1)
                EvaluateRouteMultiTrip(solution, vehicle_type_to_swap2, vehicle_id_to_swap2)
                 
            else:
                 
                EvaluateRouteSingleTrip(solution, vehicle_type_to_swap1, vehicle_id_to_swap1)
                EvaluateRouteSingleTrip(solution, vehicle_type_to_swap2, vehicle_id_to_swap2)
                 
                 
            #print "After swapping: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
            #print "Após a troca:" & solution.net_profit & "" & improvement_iterations' solution.feasible
             
    
            if vehicle_type_to_relocate1 != -1 :
                vertex = solution.route_vertices[position_to_relocate1, vehicle_type_to_relocate1, vehicle_id_to_relocate1]
    
                RemoveVertex(solution, vehicle_type_to_relocate1, vehicle_id_to_relocate1, position_to_relocate1)
                AddVertex(solution, vertex, vehicle_type_to_relocate2, vehicle_id_to_relocate2, position_to_relocate2)
                 
                #print "After relocating: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                #print "Depois de realocar:" & solution.net_profit & "" & improvement_iterations 'solution.feasible
             
             
            if vehicle_type_for_2opt1 != -1 :
    
                vertex_cnt_for_2opt1 = solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1] - position_for_2opt1
                vertex_cnt_for_2opt2 = solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2] - position_for_2opt2
    
                #For vertex = position_for_2opt1 + 1 To .route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                for vertex in range(position_for_2opt1, solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]):
                    vertex_buffer[vertex] = solution.route_vertices[vertex, vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                
    
                #For vertex = position_for_2opt2 + 1 To .route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2]
                for vertex in range(position_for_2opt2, solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2]):
                    solution.route_vertices[position_for_2opt1 + vertex - position_for_2opt2, vehicle_type_for_2opt1, vehicle_id_for_2opt1] = solution.route_vertices[vertex, vehicle_type_for_2opt2, vehicle_id_for_2opt2]
                
    
                #For vertex = position_for_2opt1 + 1 To .route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]
                for vertex in range(position_for_2opt1, solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1]):
                    solution.route_vertices[position_for_2opt2 + vertex - position_for_2opt1, vehicle_type_for_2opt2, vehicle_id_for_2opt2] = vertex_buffer[vertex]
                
    
                solution.route_vertex_cnt[vehicle_type_for_2opt1, vehicle_id_for_2opt1] = position_for_2opt1 + vertex_cnt_for_2opt2
                solution.route_vertex_cnt[vehicle_type_for_2opt2, vehicle_id_for_2opt2] = position_for_2opt2 + vertex_cnt_for_2opt1
    
                if reversal_for_2opt1 == 1 :
    
                    i = vehicle_type_for_2opt1
                    j = vehicle_id_for_2opt1
                    k = position_for_2opt1
    
                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[i, j] - (k + 1)) / 2
    
                    #For vertex = 0 To midpoint_for_chain_reversal
                    for vertex in range(0, midpoint_for_chain_reversal):
                        vertex_to_swap = solution.route_vertices[k + 1 + vertex, i, j]
                        solution.route_vertices[k + 1 + vertex, i, j] = solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j]
                        solution.route_vertices[solution.route_vertex_cnt[i, j] - vertex, i, j] = vertex_to_swap
                    
                
    
                if reversal_for_2opt2 == 1 :
    
                    a = vehicle_type_for_2opt2
                    b = vehicle_id_for_2opt2
                    c = position_for_2opt2
    
                    midpoint_for_chain_reversal = (solution.route_vertex_cnt[a, b] - (c + 1)) / 2
    
                    #For vertex = 0 To midpoint_for_chain_reversal
                    for vertex in range(0, midpoint_for_chain_reversal):
                        vertex_to_swap = solution.route_vertices[c + 1 + vertex, a, b]
                        solution.route_vertices[c + 1 + vertex, a, b] = solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b]
                        solution.route_vertices[solution.route_vertex_cnt[a, b] - vertex, a, b] = vertex_to_swap
                    
                
    
                if instance.multi_trip == True :
                    
                    EvaluateRouteMultiTrip(solution, vehicle_type_for_2opt1, vehicle_id_for_2opt1)
                    EvaluateRouteMultiTrip(solution, vehicle_type_for_2opt2, vehicle_id_for_2opt2)
                
                else:
                
                    EvaluateRouteSingleTrip(solution, vehicle_type_for_2opt1, vehicle_id_for_2opt1)
                    EvaluateRouteSingleTrip(solution, vehicle_type_for_2opt2, vehicle_id_for_2opt2)
    
                
                
                #print "2-opt with reversals: " & reversal_for_2opt1 & " " & reversal_for_2opt2
                #priint "After 2-opt: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                
                #print "2-opt with reversals:" & reversal_for_2opt1 & "" & reversal_for_2opt2
                #print "Após 2 opções:" & solution.net_profit & "" & improvement_iterations' solution.feasible
                 
             
    
            if vehicle_type_for_chain_reversal != -1 :
    
                midpoint_for_chain_reversal = (position_for_chain_reversal2 - position_for_chain_reversal1) / 2
    
                #For vertex = 0 To midpoint_for_chain_reversal
                for vertex in range(0, midpoint_for_chain_reversal):
                    vertex_to_swap = solution.route_vertices[position_for_chain_reversal1 + vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal]
                    solution.route_vertices[position_for_chain_reversal1 + vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal] = solution.route_vertices[position_for_chain_reversal2 - vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal]
                    solution.route_vertices[position_for_chain_reversal2 - vertex, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal] = vertex_to_swap
                
    
                if instance.multi_trip == True :
                
                    EvaluateRouteMultiTrip(solution, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal)
                    
                else:
                
                    EvaluateRouteSingleTrip(solution, vehicle_type_for_chain_reversal, vehicle_id_for_chain_reversal)
                
                
    
                #print "After chain reversal: " & solution.net_profit & " " & improvement_iterations 'solution.feasible
                #print "Após a reversão da cadeia:" & solution.net_profit & "" & improvement_iterations' solution.feasible
             
             
            if vehicle_type_for_full_swap1 != -1:
    
                max_vertex_cnt = solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1]
                                  
                if max_vertex_cnt < solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]:
                    max_vertex_cnt = solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]
                
                
                #For vertex = 1 To max_vertex_cnt
                for vertex in range(0, max_vertex_cnt):
                    vertex_to_swap = solution.route_vertices[vertex, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1]
                    solution.route_vertices[vertex, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1] = solution.route_vertices[vertex, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]
                    solution.route_vertices[vertex, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2] = vertex_to_swap
                
                
                vertex_cnt_to_swap = solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1]
                solution.route_vertex_cnt[vehicle_type_for_full_swap1, vehicle_id_for_full_swap1] = solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2]
                solution.route_vertex_cnt[vehicle_type_for_full_swap2, vehicle_id_for_full_swap2] = vertex_cnt_to_swap
                
                if instance.multi_trip == True :
                
                    EvaluateRouteMultiTrip(solution, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1)
                    EvaluateRouteMultiTrip(solution, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2)
                
                else:
                
                    EvaluateRouteSingleTrip(solution, vehicle_type_for_full_swap1, vehicle_id_for_full_swap1)
                    EvaluateRouteSingleTrip(solution, vehicle_type_for_full_swap2, vehicle_id_for_full_swap2)
    
                
                #print "After full swap: " & solution.net_profit & " " & solution.feasible
                #print "Após a troca completa:" & solution.net_profit & "" & solution.feasible
             
    
        
        improvement_iterations = improvement_iterations + 1

        if ((vehicle_type_to_swap1 != -1) or (vehicle_type_to_relocate1 != -1) or (vehicle_type_for_2opt1 != -1) or (vehicle_type_for_chain_reversal != -1) or (vehicle_type_for_full_swap1 != -1)) and (improvement_iterations <= max_improvement_iterations):
            break

    EvaluateSolution(solution)