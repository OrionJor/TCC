from numpy import blackman
from Bases_base import *
from In_solution import *
from Get_m import *


def EvaluateRouteMultiTrip(solution, vehicle_type_index, vehicle_id):

    #represenatar que é Double 0.0
    vehicle_capacity = 0.0
    
    min_residual_capacity = 0.0
    total_pickup_load = 0.0
    
    distance_traversed = 0.0
    duration_multiplier = 0.0
    modified_arc_duration = 0.0
    
    time_accumulated = 0
    driving_time_total = 0
    working_time_total = 0
    
    net_profit_this_route = 0.0
    total_distance_this_route = 0.0
    origin_base_id = 0
    return_base_id = 0
    this_vertex = 0
    previous_vertex =0
    
    stage = 0
    k = 0

    
    start_vertex_index = 0
    end_vertex_index = 0

    feasibility_flag = True

    #para saber de onde vem os dados
    #vehicle_type_list = GetVehicleTypeData()

    origin_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].origin_base_id
    return_base_id = origin_base_id

    vehicle_capacity = vehicle_type_list.vehicle_types[vehicle_type_index].capacity

    #para testes depois tirar
    solution = Solution_Data()

    solution.net_profit = solution.net_profit - solution.net_profit_per_route[vehicle_type_index, vehicle_id]
    net_profit_this_route = 0

    solution.total_distance = solution.total_distance - solution.total_distance_per_route[vehicle_type_index, vehicle_id]
    total_distance_this_route = 0

    #para saber de onde vem os dados
    #vertex_list = GetVertexData()

    #para saber de onde vem os dados
    #instance = GetInstanceData()

    if solution.route_vertex_cnt[vehicle_type_index, vehicle_id] > 0:

        #DP aqui
        #recursão para trás
        stage = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
        for i in range(stage, 1, -1): # segmento começando com a visita "stage"
            DP_list.control[stage] = stage
            DP_list.value[stage] = instance.penalty 

            total_pickup_load = 0
            min_residual_capacity = vehicle_capacity

            distance_traversed = 0

            for k in range(stage, solution.route_vertex_cnt[vehicle_type_index, vehicle_id] ): #possíveis índices para retornar ao depósito
                this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]

                if k == stage:
                    previous_vertex = origin_base_id
                else:
                    previous_vertex = solution.route_vertices[k-1,vehicle_type_index, vehicle_id]

                #Carregar

                min_residual_capacity = min_residual_capacity - vertex_list.vertices[this_vertex].delivery_amount

                total_pickup_load = total_pickup_load + vertex_list.vertices[this_vertex].pickup_amount

                if total_pickup_load < - epsilon:
                    #GoTo NextStage
                    pass

                if (min_residual_capacity > (vehicle_capacity - total_pickup_load)):
                    min_residual_capacity = vehicle_capacity - total_pickup_load


                if min_residual_capacity < - epsilon:
                    #GoTo NextStage
                    pass

                if ((instance.backhauls == True) and (k > stage) and (vertex_list.vertices[previous_vertex].pichup_amount > 0) and (vertex_list.vertices[this_vertex].delivery_amount > 0)):
                    #GoTo NextStage
                    pass

                #distância

                distance_traversed = distance_traversed + arc_list.distance(previous_vertex, this_vertex)

                #valor e controle
                
                if ( k  == solution.route_vertex_cnt[vehicle_type_index, vehicle_id]):  #condição de contorno
                    DP_list.control[stage] = k
                    DP_list.value[stage] = distance_traversed + arc_list.distance[this_vertex, return_base_id]

                elif k == stage: #solução titular para o stage
                    DP_list.control[stage] = k
                    DP_list.value[stage] = distance_traversed + arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1]
                
                else:
                    if (DP_list.value[stage] > (distance_traversed + arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1])): #atualizar o titular
                        DP_list.control[stage] = k
                        DP_list.value[stage] = distance_traversed +  arc_list.distance[this_vertex, return_base_id] + DP_list.value[k+1]


def NextStage(solution, vehicle_type_index, vehicle_id, stage, vehicle_capacity, origin_base_id, return_base_id):

    #agora avalie a rota com base no controle ideal
    stage += 1 
    
    distance_traversed = 0
    distance_traversed = 0
    driving_time_total = 0
    working_time_total = 0
    feasibility_flag = True

    time_accumulated = vehicle_type_list.vehicle_types[vehicle_type_index].work_start_time
    duration_multiplier = vehicle_type_list.vehicle_types[vehicle_type_index].duration_multiplier

    net_profit_this_route = (-vehicle_type_list.vehicle_types[vehicle_type_index].fixed_cost_per_trip)

    end_vertex_index = 0

    #para testes depois tirar
    solution = Solution_Data()

    while True:

        start_vertex_index = end_vertex_index + 1
        end_vertex_index = DP_list.control(start_vertex_index)

        total_pickup_load = 0
        min_residual_capacity = vehicle_capacity

        
        for k in range(start_vertex_index, end_vertex_index):

            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]

            if instance.vehicle_location_incompatibility == True:
                if vehicle_type_list.compatible(this_vertex, vehicle_type_index) == False:
                        feasibility_flag = False
                        solution.feasible = False
                        net_profit_this_route = net_profit_this_route - instance.penalty
                     
            min_residual_capacity = min_residual_capacity - vertex_list.vertices[this_vertex].delivery_amount
            total_pickup_load = total_pickup_load + vertex_list.vertices[this_vertex].pickup_amount

            if total_pickup_load < -epsilon:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - instance.penalty * ((((-total_pickup_load) / (vehicle_capacity + epsilon) + 1) ^ 2) - 1)
                    

            if min_residual_capacity > vehicle_capacity - total_pickup_load:
                min_residual_capacity = vehicle_capacity - total_pickup_load
                    

            if min_residual_capacity < -epsilon:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - instance.penalty * ((((-min_residual_capacity) / (vehicle_capacity + epsilon) + 1) ^ 2) - 1)
                    

            net_profit_this_route = net_profit_this_route + vertex_list.vertices(this_vertex).profit

            if k == start_vertex_index:

                modified_arc_duration = arc_list.duration[origin_base_id, this_vertex] * duration_multiplier

                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration

                distance_traversed = distance_traversed + arc_list.distance[origin_base_id, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[origin_base_id, this_vertex]



            else:
                previous_vertex = arc_list.route_vertices[ k - 1,vehicle_type_index, vehicle_id]

                modified_arc_duration = arc_list.duration[previous_vertex, this_vertex] * duration_multiplier

                time_accumulated = time_accumulated + modified_arc_duration
                driving_time_total = driving_time_total + modified_arc_duration
                working_time_total = working_time_total + modified_arc_duration

                distance_traversed = distance_traversed + arc_list.distance[previous_vertex, this_vertex]
                total_distance_this_route = total_distance_this_route + arc_list.distance[previous_vertex, this_vertex]


                if instance.backhauls == True and ((-1 *vertex_list.vertices[previous_vertex].pickup_amount) > 0) and vertex_list.vertices(this_vertex).delivery_amount > 0:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - instance.penalty
                        

                    

            if time_accumulated < vertex_list.vertices[this_vertex].time_window_start:

                working_time_total = working_time_total + vertex_list.vertices[this_vertex].time_window_start - time_accumulated
                time_accumulated = vertex_list.vertices[this_vertex].time_window_start

                    

            time_accumulated = time_accumulated + vertex_list.vertices[this_vertex].service_time
            working_time_total = working_time_total + vertex_list.vertices[this_vertex].service_time

            if time_accumulated > vertex_list.vertices[this_vertex].time_window_end:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False
                        
                    net_profit_this_route = net_profit_this_route - instance.penalty * (((time_accumulated / vertex_list.vertices[this_vertex].time_window_end) ^ 2) - 1)
                    

        

        modified_arc_duration = arc_list.duration[this_vertex, return_base_id] * duration_multiplier

        time_accumulated = time_accumulated + modified_arc_duration
        driving_time_total = driving_time_total + modified_arc_duration
        working_time_total = working_time_total + modified_arc_duration

        distance_traversed = distance_traversed + arc_list.distance(this_vertex, return_base_id)
        total_distance_this_route = total_distance_this_route + arc_list.distance(this_vertex, return_base_id)
                
        if solution.route_vertex_cnt(vehicle_type_index, vehicle_id) > end_vertex_index:
            time_accumulated = time_accumulated + vertex_list.vertices(return_base_id).service_time
            working_time_total = working_time_total + vertex_list.vertices(return_base_id).service_time
        
        if end_vertex_index != solution.route_vertex_cnt[vehicle_type_index, vehicle_id]:
            break

    
    if time_accumulated > vertex_list.vertices[return_base_id].time_window_end:
        if instance.soft_time_windows == False:
            feasibility_flag = False
            solution.feasible = False
     
            net_profit_this_route = net_profit_this_route - instance.penalty * (((time_accumulated / vertex_list.vertices[return_base_id].time_window_end) ^ 2) - 1)
 
                
    if distance_traversed > vehicle_type_list.vehicle_types[vehicle_type_index].distance_limit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - instance.penalty * (((distance_traversed / vehicle_type_list.vehicle_types[vehicle_type_index].distance_limit) ^ 2) - 1)
 

    if driving_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].driving_time_limit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - instance.penalty * (((driving_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].driving_time_limit) ^ 2) - 1)
 

    if working_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].working_time_limit:
        feasibility_flag = False
        solution.feasible = False
        net_profit_this_route = net_profit_this_route - instance.penalty * (((working_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].working_time_limit) ^ 2) - 1)
 


    solution.total_distance_per_route[vehicle_type_index, vehicle_id] = total_distance_this_route
    solution.total_distance = solution.total_distance + total_distance_this_route

    net_profit_this_route = net_profit_this_route - total_distance_this_route * vehicle_type_list.vehicle_types[vehicle_type_index].cost_per_unit_distance
    if feasibility_flag == False:
        net_profit_this_route = net_profit_this_route - instance.penalty

        solution.net_profit_per_route[vehicle_type_index, vehicle_id] = net_profit_this_route
        solution.net_profit = solution.net_profit + net_profit_this_route

    #print(vehicle_type_index & " " & vehicle_id & " " &)


def EvaluateRouteSingleTrip(solution, vehicle_type_index, vehicle_id):

    #para testes depois tirar
    solution = Solution_Data()
    
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

    time_accumulated = vehicle_type_list.vehicle_types[vehicle_type_index].work_start_time
    duration_multiplier = vehicle_type_list.vehicle_types[vehicle_type_index].duration_multiplier

    solution.net_profit = solution.net_profit - solution.net_profit_per_route[vehicle_type_index, vehicle_id]
    net_profit_this_route = 0
        
    solution.total_distance = solution.total_distance - solution.total_distance_per_route[vehicle_type_index, vehicle_id]
    total_distance_this_route = 0

    if solution.route_vertex_cnt[vehicle_type_index, vehicle_id] > 0:
        
        net_profit_this_route = -vehicle_type_list.vehicle_types[vehicle_type_index].fixed_cost_per_trip
        origin_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].origin_base_id
        return_base_id = vehicle_type_list.vehicle_types[vehicle_type_index].return_base_id

        for k in range(0, solution.route_vertex_cnt[vehicle_type_index, vehicle_id]):

            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]
            delivery_amount = delivery_amount + vertex_list.vertices[this_vertex].delivery_amount

        
        if delivery_amount > vehicle_type_list.vehicle_types[vehicle_type_index].capacity:
            
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - instance.penalty * (((delivery_amount / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ^ 2) - 1)

        for k in range(0, solution.route_vertex_cnt[vehicle_type_index, vehicle_id]):

            this_vertex = solution.route_vertices[k, vehicle_type_index, vehicle_id]
                
            if instance.vehicle_location_incompatibility == True:
                if vehicle_type_list.compatible[this_vertex, vehicle_type_index] == False:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - instance.penalty
                
            pickup_amount = pickup_amount + vertex_list.vertices[this_vertex].pickup_amount
            delivery_amount = delivery_amount - vertex_list.vertices[this_vertex].delivery_amount


            if pickup_amount + delivery_amount > vehicle_type_list.vehicle_types[vehicle_type_index].capacity:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - instance.penalty * ((((pickup_amount + delivery_amount) / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ^ 2) - 1)
           
            
            
            if pickup_amount < 0:
                feasibility_flag = False
                solution.feasible = False
                net_profit_this_route = net_profit_this_route - instance.penalty * ((( (-1 *(pickup_amount)) / (vehicle_type_list.vehicle_types[vehicle_type_index].capacity + epsilon)) ^ 2) + 1)

                
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

                if instance.backhauls == True and (-1 *(vertex_list.vertices[previous_vertex].pickup_amount)) > 0 and vertex_list.vertices[this_vertex].delivery_amount > 0:
                    feasibility_flag = False
                    solution.feasible = False
                    net_profit_this_route = net_profit_this_route - instance.penalty

            if time_accumulated < vertex_list.vertices[this_vertex].time_window_start:
                working_time_total = working_time_total + vertex_list.vertices[this_vertex].time_window_start - time_accumulated
                time_accumulated = vertex_list.vertices[this_vertex].time_window_start

            time_accumulated = time_accumulated + vertex_list.vertices[this_vertex].service_time
            working_time_total = working_time_total + vertex_list.vertices[this_vertex].service_time

            if time_accumulated > vertex_list.vertices[this_vertex].time_window_end:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False
                net_profit_this_route = net_profit_this_route - instance.penalty * (((time_accumulated / vertex_list.vertices[this_vertex].time_window_end) ^ 2) - 1)


        if instance.open_vrp == False:

            this_vertex = solution.route_vertices[ solution.route_vertex_cnt(vehicle_type_index, vehicle_id),vehicle_type_index, vehicle_id]
                
            modified_arc_duration = arc_list.duration[this_vertex, return_base_id] * duration_multiplier
                
            time_accumulated = time_accumulated + modified_arc_duration
            driving_time_total = driving_time_total + modified_arc_duration
            working_time_total = working_time_total + modified_arc_duration
    
            distance_traversed = distance_traversed + arc_list.distance[this_vertex, return_base_id]
            total_distance_this_route = total_distance_this_route + arc_list.distance[this_vertex, return_base_id]

            if time_accumulated > vertex_list.vertices[return_base_id].time_window_end:
                if instance.soft_time_windows == False:
                    feasibility_flag = False
                    solution.feasible = False

                net_profit_this_route = net_profit_this_route - instance.penalty * (((time_accumulated / vertex_list.vertices[return_base_id].time_window_end) ^ 2) - 1)

        if distance_traversed > vehicle_type_list.vehicle_types[vehicle_type_index].distance_limit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - instance.penalty * (((distance_traversed / vehicle_type_list.vehicle_types[vehicle_type_index].distance_limit) ^ 2) - 1)
            
        if driving_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].driving_time_limit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - instance.penalty * (((driving_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].driving_time_limit) ^ 2) - 1)
    
        if working_time_total > vehicle_type_list.vehicle_types[vehicle_type_index].working_time_limit:
            feasibility_flag = False
            solution.feasible = False
            net_profit_this_route = net_profit_this_route - instance.penalty * (((working_time_total / vehicle_type_list.vehicle_types[vehicle_type_index].working_time_limit) ^ 2) - 1)

    solution.total_distance_per_route[vehicle_type_index, vehicle_id] = total_distance_this_route
    solution.total_distance = solution.total_distance + total_distance_this_route

    net_profit_this_route = net_profit_this_route - total_distance_this_route * vehicle_type_list.vehicle_types[vehicle_type_index].cost_per_unit_distance
    if feasibility_flag == False:
            net_profit_this_route = net_profit_this_route - instance.penalty
    
    solution.net_profit_per_route[vehicle_type_index, vehicle_id] = net_profit_this_route
    solution.net_profit = solution.net_profit + net_profit_this_route

    #print(vehicle_type_index & " " & vehicle_id & " " &)