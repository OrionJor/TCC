from Bases_base import *
from Get_m import *

def InitializeDP():
    DP_list = DP_Data()
    
    DP_list.control = np.zeros((vertex_list.num_customers), dtype='int16')
    DP_list.value = np.zeros((vertex_list.num_customers), dtype='int16')

    return DP_list

DP_list = InitializeDP()


def AddVertex2(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position, penalty):

    #solution = InitializeSolution(solution)
    #print(penalty)

    #.vertices_visited(vertex_to_be_added) = .vertices_visited(vertex_to_be_added) + 1
    
    solution.vertices_visited[vertex_to_be_added] += 1

    #print(solution.vertices_visited[vertex_to_be_added])
    
    #mudança -> 'shift
    rota_do_vertice_cnt = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
    #print(position)
    
    #https://pynative.com/python-range-function/ step maior para menor
    #inicio, fim, e step
    #for i in range(6, -1, -1): -> temos que testar
    #print(rota_do_vertice_cnt)

    #Sistema para começar da posição 1 e não da 0
    #print(position-1)
    #print(position)
    for i in range(rota_do_vertice_cnt, position, -1):#perguntar
        #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i)
        solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i - 1, vehicle_type_index, vehicle_id]
        #b,l,c = shape(solution.route_vertices)
        #aux = np.zeros((b,l,c), dtype='int32')
        #aux2= np.concatenate()  #solution.route_vertices[:-1,:,:] = aux
        #print(i)
            

        
        #dimensão, linha e coluna
    solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added
    #print(position)
    #print(solution.route_vertices[4, vehicle_type_index, vehicle_id])
    #.route_vertex_cnt(vehicle_type_index, vehicle_id) = .route_vertex_cnt(vehicle_type_index, vehicle_id) + 1

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1
    
    #print(solution.route_vertices[i, vehicle_type_index, vehicle_id])
    #saber de onde vem os dados
    #instance = GetInstanceData()
    
    if  instance.multi_trip == True:
        EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    else:
        EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    
    #print(instance.multi_trip)

    #saber de onde vem os dados
    #vertex_list = 
    #GetVertexData()

    if vertex_list.vertices[vertex_to_be_added].mandatory == 1:
        solution.net_profit = solution.net_profit + penalty
    
    #print(solution.net_profit)#vai perdendo 1 em cada vértece
    #print(vertex_list.vertices[vertex_to_be_added].mandatory)

    #objeto principal
    return solution

def RemoveVertex2(solution, vehicle_type_index, vehicle_id, position,  penalty):

    #print(penalty)


    vertex_to_removed = solution.route_vertices[position, vehicle_type_index, vehicle_id]

    solution.vertices_visited[vertex_to_removed] = solution.vertices_visited[vertex_to_removed] -1

    vertice = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
    

    for i in range(position, vertice-1): #perguntar
        #print("position", position, "vertice", vertice)
        solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i + 1, vehicle_type_index, vehicle_id]

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] = solution.route_vertex_cnt[vehicle_type_index, vehicle_id] - 1

    #saber de onde vem os dados
    #instance = GetInstanceData()
    #print(solution.route_vertex_cnt[vehicle_type_index, vehicle_id])

    if instance.multi_trip == True:
        EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    else:
        EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id, penalty)

    
    #saber de onde vem os dados
    #print(vertex_list.vertices[vertex_to_removed].mandatory)
    #vertex_list =  GetVertexData()
    if vertex_list.vertices[vertex_to_removed].mandatory == 1:
        solution.net_profit = solution.net_profit - penalty
        #print(solution.net_profit)

    return solution





def EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id, penalty):

    net_profit_this_route = 0
    total_distance_this_route = 0
    origin_base_id = 0
    return_base_id = 0
    this_vertex = 0
    previous_vertex = 0 
    
    
    delivery_amount = 0
    pickup_amount = 0
    distance_traversed = 0
    driving_time_total = 0
    working_time_total = 0
    feasibility_flag = True

    time_accumulated = vehicle_type_list.vehicle_types[vehicle_type_index].WorkStartTime
    duration_multiplier = vehicle_type_list.vehicle_types[vehicle_type_index].DurationMultiplier

    solution.net_profit = solution.net_profit - solution.net_profit_per_route[vehicle_type_index, vehicle_id]
    net_profit_this_route = 0
        
    solution.total_distance = solution.total_distance - solution.total_distance_per_route[vehicle_type_index, vehicle_id]
    total_distance_this_route = 0

    if solution.route_vertex_cnt[vehicle_type_index, vehicle_id] > 0:
        
        net_profit_this_route = ( -vehicle_type_list.vehicle_types[vehicle_type_index].FixedCostPerTrip)
        origin_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].OriginBaseId
        return_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].ReturnBaseId

        #For k = 1 To .route_vertex_cnt(vehicle_type_index, vehicle_id)
        for k in range(0, solution.route_vertex_cnt[vehicle_type_index, vehicle_id]):

            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]
            delivery_amount = delivery_amount + vertex_list.vertices[this_vertex].DeliveryAmount

        
        if delivery_amount > vehicle_type_list.vehicle_types[vehicle_type_index].capacity:
            
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - penalty * (((delivery_amount / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ** 2) - 1)

        #For k = 1 To .route_vertex_cnt(vehicle_type_index, vehicle_id)
        for k in range(0, solution.route_vertex_cnt[vehicle_type_index, vehicle_id]):

            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]
                
            if instance.vehicle_location_incompatibility == True:
                if vehicle_type_list.compatible[this_vertex, vehicle_type_index] == False:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty
                
            pickup_amount = pickup_amount + vertex_list.vertices[this_vertex].PickupAmount
            delivery_amount = delivery_amount - vertex_list.vertices[this_vertex].DeliveryAmount


            if (pickup_amount + delivery_amount) > vehicle_type_list.vehicle_types[vehicle_type_index].capacity:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - penalty * ((((pickup_amount + delivery_amount) / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ** 2) - 1)
           
            
            
            if pickup_amount < 0:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - penalty * ((( (abs(pickup_amount)) / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ** 2) + 1)

                
            net_profit_this_route = net_profit_this_route + vertex_list.vertices[this_vertex].profit

            if k == 0:
                #if k == 1: anterior

                modified_arc_duration = arc_list.duration[origin_base_id, this_vertex] * duration_multiplier
                
                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration
        
                distance_traversed = distance_traversed + arc_list.distance[origin_base_id, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[origin_base_id, this_vertex]

            else:
                previous_vertex = solution.route_vertices[k - 1, vehicle_type_index, vehicle_id]

                modified_arc_duration = arc_list.duration[previous_vertex, this_vertex] * duration_multiplier
                
                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration
        
                distance_traversed = distance_traversed + arc_list.distance[previous_vertex, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[previous_vertex, this_vertex]

                if (instance.backhauls == True) and ((abs(vertex_list.vertices[previous_vertex].PickupAmount)) > 0) and vertex_list.vertices[this_vertex].DeliveryAmount > 0:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty

            if time_accumulated < vertex_list.vertices[this_vertex].TimeWindowsStart:
                working_time_total = working_time_total + vertex_list.vertices[this_vertex].TimeWindowsStart - time_accumulated
                time_accumulated = vertex_list.vertices[this_vertex].TimeWindowsStart

            time_accumulated = time_accumulated + vertex_list.vertices[this_vertex].ServiceTime
            working_time_total = working_time_total + vertex_list.vertices[this_vertex].ServiceTime

            if time_accumulated > vertex_list.vertices[this_vertex].TimeWindowsEnd:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False
                net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[this_vertex].TimeWindowsEnd) ** 2) - 1)


        if instance.open_vrp == False:

            this_vertex = solution.route_vertices[ (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1), vehicle_type_index, vehicle_id]
                
            modified_arc_duration = arc_list.duration[this_vertex, return_base_id] * duration_multiplier
                
            time_accumulated = time_accumulated + modified_arc_duration
            driving_time_total = driving_time_total + modified_arc_duration
            working_time_total = working_time_total + modified_arc_duration
    
            distance_traversed = distance_traversed + arc_list.distance[this_vertex, return_base_id]
            total_distance_this_route = total_distance_this_route + arc_list.distance[this_vertex, return_base_id]

            if time_accumulated > vertex_list.vertices[return_base_id].TimeWindowsEnd:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False

                net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[return_base_id].TimeWindowsEnd) ** 2) - 1)

        if distance_traversed > vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - penalty * (((distance_traversed / vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit) ** 2) - 1)
            
        if driving_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - penalty * (((driving_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit) ** 2) - 1)
    
        if working_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - penalty * (((working_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit) ** 2) - 1)

    solution.total_distance_per_route[vehicle_type_index, vehicle_id] = total_distance_this_route
    solution.total_distance = solution.total_distance + total_distance_this_route

    net_profit_this_route = net_profit_this_route - total_distance_this_route * vehicle_type_list.vehicle_types[vehicle_type_index].CostPerUnitDistance
    if feasibility_flag == False:
        net_profit_this_route = net_profit_this_route - penalty
    
    solution.net_profit_per_route[vehicle_type_index, vehicle_id] = net_profit_this_route
    solution.net_profit = solution.net_profit + net_profit_this_route

    return solution

def EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id, penalty):

    #represenatar que é Double 0.0 ou 0
    vehicle_capacity = 0
    
    min_residual_capacity = 0
    total_pickup_load = 0
    
    distance_traversed = 0
    duration_multiplier = 0
    modified_arc_duration = 0
    
    time_accumulated = 0
    driving_time_total = 0
    working_time_total = 0
    
    net_profit_this_route = 0
    total_distance_this_route = 0
    origin_base_id = 0
    return_base_id = 0
    this_vertex = 0
    previous_vertex = 0
    
    stage = 0
    k = 0

    
    start_vertex_index = 0
    end_vertex_index = 0

    feasibility_flag = True

    #para saber de onde vem os dados
    #vehicle_type_list = 
    #GetVehicleTypeData()

    origin_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].OriginBaseId
    return_base_id = origin_base_id

    vehicle_capacity = vehicle_type_list.vehicle_types[vehicle_type_index].capacity

    solution.net_profit = solution.net_profit - solution.net_profit_per_route[vehicle_type_index, vehicle_id]
    net_profit_this_route = 0

    solution.total_distance = solution.total_distance - solution.total_distance_per_route[vehicle_type_index, vehicle_id]
    total_distance_this_route = 0

    #para saber de onde vem os dados
    #vertex_list = 
    #GetVertexData()

    #para saber de onde vem os dados
    #instance = 
    #GetInstanceData()
    #InitializeSolution(solution)
    
    route_vertex_cnt = 0

    if solution.route_vertex_cnt[vehicle_type_index, vehicle_id] > 0:

        #DP aqui
        #recursão para trás
        route_vertex_cnt = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
        
        #For stage = .route_vertex_cnt(vehicle_type_index, vehicle_id) To 1 Step -1 ' segment starting with visiting "stage"
        for stage in range(route_vertex_cnt-1, -1, -1): # segmento começando com a visita "stage"

            DP_list.control[stage] = stage
            DP_list.value[stage] = penalty 

            total_pickup_load = 0
            min_residual_capacity = vehicle_capacity

            distance_traversed = 0
            

            for k in range(stage, solution.route_vertex_cnt[vehicle_type_index, vehicle_id]): #possíveis índices para retornar ao depósito

                this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]

                if k == stage:
                    previous_vertex = origin_base_id
                else:
                    previous_vertex = solution.route_vertices[k-1, vehicle_type_index, vehicle_id]

                #Carregar

                min_residual_capacity = min_residual_capacity - vertex_list.vertices[this_vertex].DeliveryAmount

                total_pickup_load = total_pickup_load + vertex_list.vertices[this_vertex].PickupAmount

                
                if total_pickup_load < (-epsilon):
                    NextStage(solution, vehicle_type_index, vehicle_id, stage, vehicle_capacity, origin_base_id, return_base_id, penalty)

                if (min_residual_capacity > (vehicle_capacity - total_pickup_load)):
                    min_residual_capacity = vehicle_capacity - total_pickup_load
        
                if min_residual_capacity < - epsilon:
                    NextStage(solution, vehicle_type_index, vehicle_id, stage, vehicle_capacity, origin_base_id, return_base_id, penalty)

                if ((instance.backhauls == True) and (k > stage) and (vertex_list.vertices[previous_vertex].PickupAmount > 0) and (vertex_list.vertices[this_vertex].DeliveryAmount > 0)):
                    NextStage(solution, vehicle_type_index, vehicle_id, stage, vehicle_capacity, origin_base_id, return_base_id, penalty)

                #distância

                distance_traversed = distance_traversed + arc_list.distance[previous_vertex, this_vertex]

                #valor e controle
                
                if ( k  == (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1 )):  #condição de contorno
                    DP_list.control[stage] = k
                    DP_list.value[stage] = distance_traversed + arc_list.distance[this_vertex, return_base_id]

                elif k == stage: #solução titular para o stage
                    DP_list.control[stage] = k
                    DP_list.value[stage] = distance_traversed + arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1]
                
                else:
                    if (DP_list.value[stage] > (distance_traversed + arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1])): #atualizar o titular
                        DP_list.control[stage] = k
                        DP_list.value[stage] = distance_traversed +  arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1]


        #agora avalie a rota com base no controle ideal
        distance_traversed = 0
        driving_time_total = 0
        working_time_total = 0
        feasibility_flag = True

        time_accumulated = vehicle_type_list.vehicle_types[vehicle_type_index].WorkStartTime
        duration_multiplier = vehicle_type_list.vehicle_types[vehicle_type_index].DurationMultiplier

        net_profit_this_route = (-vehicle_type_list.vehicle_types[vehicle_type_index].FixedCostPerTrip)

        #end_vertex_index = 0
        end_vertex_index = -1

        
        while True:
            
            start_vertex_index = end_vertex_index + 1
            end_vertex_index = DP_list.control[start_vertex_index]

            total_pickup_load = 0
            min_residual_capacity = vehicle_capacity

            
            #For k = start_vertex_index To end_vertex_index
            for k in range(start_vertex_index, end_vertex_index + 1):
                
                this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]

                if instance.vehicle_location_incompatibility == True:
                    if vehicle_type_list.compatible[this_vertex, vehicle_type_index] == False:
                        feasibility_flag = False
                        solution.feasible = False
                        net_profit_this_route = net_profit_this_route - penalty
                        
                min_residual_capacity = min_residual_capacity - vertex_list.vertices[this_vertex].DeliveryAmount
                total_pickup_load = total_pickup_load + vertex_list.vertices[this_vertex].PickupAmount

                if total_pickup_load < -epsilon:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty * ((((-total_pickup_load) / (vehicle_capacity + epsilon) + 1) ** 2) - 1)
                        

                if min_residual_capacity > vehicle_capacity - total_pickup_load:
                    min_residual_capacity = vehicle_capacity - total_pickup_load
                        

                if min_residual_capacity < -epsilon:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty * ((((-min_residual_capacity) / (vehicle_capacity + epsilon) + 1) ** 2) - 1)
                        

                net_profit_this_route = net_profit_this_route + vertex_list.vertices[this_vertex].profit

                if k == start_vertex_index:

                    modified_arc_duration = arc_list.duration[origin_base_id, this_vertex] * duration_multiplier

                    time_accumulated = time_accumulated + modified_arc_duration
                    driving_time_total = driving_time_total + modified_arc_duration
                    working_time_total = working_time_total + modified_arc_duration

                    distance_traversed = distance_traversed + arc_list.distance[origin_base_id, this_vertex]
                    total_distance_this_route = total_distance_this_route + arc_list.distance[origin_base_id, this_vertex]



                else:
                    previous_vertex = solution.route_vertices[ k - 1,vehicle_type_index, vehicle_id]

                    modified_arc_duration = arc_list.duration[previous_vertex, this_vertex] * duration_multiplier

                    time_accumulated = time_accumulated + modified_arc_duration
                    driving_time_total = driving_time_total + modified_arc_duration
                    working_time_total = working_time_total + modified_arc_duration

                    distance_traversed = distance_traversed + arc_list.distance[previous_vertex, this_vertex]
                    total_distance_this_route = total_distance_this_route + arc_list.distance[previous_vertex, this_vertex]


                    if instance.backhauls == True and ( abs(vertex_list.vertices[previous_vertex].PickupAmount) > 0) and vertex_list.vertices[this_vertex].delivery_amount > 0:
                        feasibility_flag = False
                        solution.feasible = False
                        net_profit_this_route = net_profit_this_route - penalty
                            

                        

                if time_accumulated < vertex_list.vertices[this_vertex].TimeWindowsStart:

                    working_time_total = working_time_total + vertex_list.vertices[this_vertex].TimeWindowsStart - time_accumulated
                    time_accumulated = vertex_list.vertices[this_vertex].TimeWindowsStart

                        

                time_accumulated = time_accumulated + vertex_list.vertices[this_vertex].ServiceTime
                working_time_total = working_time_total + vertex_list.vertices[this_vertex].ServiceTime

                if time_accumulated > vertex_list.vertices[this_vertex].TimeWindowsEnd:
                    if instance.soft_time_windows == False:
                        feasibility_flag = False
                        solution.feasible = False
                            
                    net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[this_vertex].TimeWindowsEnd) ** 2) - 1)
                        

            

            modified_arc_duration = arc_list.duration[this_vertex, return_base_id] * duration_multiplier

            time_accumulated = time_accumulated + modified_arc_duration
            driving_time_total = driving_time_total + modified_arc_duration
            working_time_total = working_time_total + modified_arc_duration

            distance_traversed = distance_traversed + arc_list.distance[this_vertex, return_base_id]
            total_distance_this_route = total_distance_this_route + arc_list.distance[this_vertex, return_base_id]
                    
            if (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1 ) > end_vertex_index:
                time_accumulated = time_accumulated + vertex_list.vertices[return_base_id].ServiceTime
                working_time_total = working_time_total + vertex_list.vertices[return_base_id].ServiceTime
            
            if end_vertex_index == (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1):
                break

    if time_accumulated > vertex_list.vertices[return_base_id].TimeWindowsEnd:
        if instance.soft_time_windows == False:
            feasibility_flag = False
            solution.feasible = False
     
        net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[return_base_id].TimeWindowsEnd) ** 2) - 1)
 
                
    if distance_traversed > vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((distance_traversed / vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit) ** 2) - 1)
 

    if driving_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((driving_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit) ** 2) - 1)
 

    if working_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((working_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit) ** 2) - 1)
 


    solution.total_distance_per_route[vehicle_type_index, vehicle_id] = total_distance_this_route
    solution.total_distance = solution.total_distance + total_distance_this_route

    net_profit_this_route = net_profit_this_route - total_distance_this_route * vehicle_type_list.vehicle_types[vehicle_type_index].CostPerUnitDistance
    if feasibility_flag == False:
        net_profit_this_route = net_profit_this_route - penalty

    solution.net_profit_per_route[vehicle_type_index, vehicle_id] = net_profit_this_route
    solution.net_profit = solution.net_profit + net_profit_this_route
    #print(vehicle_type_index & " " & vehicle_id & " " &)

    return solution


def NextStage(solution, vehicle_type_index, vehicle_id, stage, vehicle_capacity, origin_base_id, return_base_id, penalty):

    #agora avalie a rota com base no controle ideal
    distance_traversed = 0
    driving_time_total = 0
    working_time_total = 0
    feasibility_flag = True

    time_accumulated = vehicle_type_list.vehicle_types[vehicle_type_index].WorkStartTime
    duration_multiplier = vehicle_type_list.vehicle_types[vehicle_type_index].DurationMultiplier

    net_profit_this_route = (-vehicle_type_list.vehicle_types[vehicle_type_index].FixedCostPerTrip)

    #end_vertex_index = 0
    end_vertex_index = -1

        
    while True:
            
        start_vertex_index = end_vertex_index + 1
        end_vertex_index = DP_list.control[start_vertex_index]

        total_pickup_load = 0
        min_residual_capacity = vehicle_capacity

            
        #For k = start_vertex_index To end_vertex_index
        for k in range(start_vertex_index, end_vertex_index + 1):
                
            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]

            if instance.vehicle_location_incompatibility == True:
                if vehicle_type_list.compatible[this_vertex, vehicle_type_index] == False:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty
                        
            min_residual_capacity = min_residual_capacity - vertex_list.vertices[this_vertex].DeliveryAmount
            total_pickup_load = total_pickup_load + vertex_list.vertices[this_vertex].PickupAmount

            if total_pickup_load < -epsilon:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - penalty * ((((-total_pickup_load) / (vehicle_capacity + epsilon) + 1) ** 2) - 1)
                        

            if min_residual_capacity > vehicle_capacity - total_pickup_load:
                min_residual_capacity = vehicle_capacity - total_pickup_load
                        

            if min_residual_capacity < -epsilon:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - penalty * ((((-min_residual_capacity) / (vehicle_capacity + epsilon) + 1) ** 2) - 1)
                        

            net_profit_this_route = net_profit_this_route + vertex_list.vertices[this_vertex].profit

            if k == start_vertex_index:

                modified_arc_duration = arc_list.duration[origin_base_id, this_vertex] * duration_multiplier

                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration

                distance_traversed = distance_traversed + arc_list.distance[origin_base_id, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[origin_base_id, this_vertex]



            else:
                previous_vertex = solution.route_vertices[ k - 1,vehicle_type_index, vehicle_id]

                modified_arc_duration = arc_list.duration[previous_vertex, this_vertex] * duration_multiplier

                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration

                distance_traversed = distance_traversed + arc_list.distance[previous_vertex, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[previous_vertex, this_vertex]


                if instance.backhauls == True and (abs(vertex_list.vertices[previous_vertex].PickupAmount) > 0) and vertex_list.vertices[this_vertex].delivery_amount > 0:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - penalty
                            

                        

            if time_accumulated < vertex_list.vertices[this_vertex].TimeWindowsStart:

                working_time_total = working_time_total + vertex_list.vertices[this_vertex].TimeWindowsStart - time_accumulated
                time_accumulated = vertex_list.vertices[this_vertex].TimeWindowsStart

                        

            time_accumulated = time_accumulated + vertex_list.vertices[this_vertex].ServiceTime
            working_time_total = working_time_total + vertex_list.vertices[this_vertex].ServiceTime

            if time_accumulated > vertex_list.vertices[this_vertex].TimeWindowsEnd:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False
                            
                net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[this_vertex].TimeWindowsEnd) ** 2) - 1)
                        

            

            modified_arc_duration = arc_list.duration[this_vertex, return_base_id] * duration_multiplier

            time_accumulated = time_accumulated + modified_arc_duration
            driving_time_total = driving_time_total + modified_arc_duration
            working_time_total = working_time_total + modified_arc_duration

            distance_traversed = distance_traversed + arc_list.distance[this_vertex, return_base_id]
            total_distance_this_route = total_distance_this_route + arc_list.distance[this_vertex, return_base_id]
                    
            if (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1 ) > end_vertex_index:
                time_accumulated = time_accumulated + vertex_list.vertices[return_base_id].ServiceTime
                working_time_total = working_time_total + vertex_list.vertices[return_base_id].ServiceTime
            
        if end_vertex_index == (solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -1):
            break

    if time_accumulated > vertex_list.vertices[return_base_id].TimeWindowsEnd:
        if instance.soft_time_windows == False:
            feasibility_flag = False
            solution.feasible = False
     
        net_profit_this_route = net_profit_this_route - penalty * (((time_accumulated / vertex_list.vertices[return_base_id].TimeWindowsEnd) ** 2) - 1)
 
                
    if distance_traversed > vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((distance_traversed / vehicle_type_list.vehicle_types[vehicle_type_index].DistanceLimit) ** 2) - 1)
 

    if driving_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((driving_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].DrivingTimeLimit) ** 2) - 1)
 

    if working_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - penalty * (((working_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].WorkingTimeLimit) ** 2) - 1)
 


    solution.total_distance_per_route[vehicle_type_index, vehicle_id] = total_distance_this_route
    solution.total_distance = solution.total_distance + total_distance_this_route

    net_profit_this_route = net_profit_this_route - total_distance_this_route * vehicle_type_list.vehicle_types[vehicle_type_index].CostPerUnitDistance
    if feasibility_flag == False:
        net_profit_this_route = net_profit_this_route - penalty

    solution.net_profit_per_route[vehicle_type_index, vehicle_id] = net_profit_this_route
    solution.net_profit = solution.net_profit + net_profit_this_route
    #print(vehicle_type_index & " " & vehicle_id & " " &)

    return solution