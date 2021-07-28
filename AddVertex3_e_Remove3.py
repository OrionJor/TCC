from Bases_base import *
from Get_m import *

def AddVertex3(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position, penalty):

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
        solution.route_vertices[i+1, vehicle_type_index, vehicle_id] = solution.route_vertices[i, vehicle_type_index, vehicle_id]
            

        
        #dimensão, linha e coluna
    solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added
    #print(position)
    #print(solution.route_vertices[4, vehicle_type_index, vehicle_id])
    #.route_vertex_cnt(vehicle_type_index, vehicle_id) = .route_vertex_cnt(vehicle_type_index, vehicle_id) + 1

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1
    
    #print(solution.route_vertices[i, vehicle_type_index, vehicle_id])
    #saber de onde vem os dados
    #instance = GetInstanceData()
    
    #if  instance.multi_trip == True:
        #EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    #else:
        #EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    
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

def RemoveVertex3(solution, vehicle_type_index, vehicle_id, position,  penalty):

    #print(penalty)


    vertex_to_removed = solution.route_vertices[position, vehicle_type_index, vehicle_id]

    solution.vertices_visited[vertex_to_removed] = solution.vertices_visited[vertex_to_removed] -1

    vertice = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
    

    print(vertice)
    #for iR in range(position, vertice): #perguntar
    #print(iR)
        #print("position", position, "vertice", vertice)
        #solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i + 1, vehicle_type_index, vehicle_id]

    #solution.route_vertex_cnt[vehicle_type_index, vehicle_id] = solution.route_vertex_cnt[vehicle_type_index, vehicle_id] - 1

    #saber de onde vem os dados
    #instance = GetInstanceData()
    #print(solution.route_vertex_cnt[vehicle_type_index, vehicle_id])

    #if instance.multi_trip == True:
        #EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id, penalty)
    #else:
        #EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id, penalty)

    
    #saber de onde vem os dados
    #print(vertex_list.vertices[vertex_to_removed].mandatory)
    #vertex_list =  GetVertexData()
    #if vertex_list.vertices[vertex_to_removed].mandatory == 1:
        #solution.net_profit = solution.net_profit - penalty
        #print(solution.net_profit)