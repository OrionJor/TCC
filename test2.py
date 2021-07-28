from Bases_base import *
from In_solution import *
from Get_m import *
from Improve_Solution import *
from Flesibility import *
from test import *
from datetime import datetime


def Add(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position, penalty):

    solution.vertices_visited[vertex_to_be_added] += 1



    #print(solution.vertices_visited[vertex_to_be_added])
    
    #mudança -> 'shift
    rota_do_vertice_cnt = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
    
    for i in range(rota_do_vertice_cnt, position, -1):#perguntar
        #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i) -> perguntar
        solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i-1, vehicle_type_index, vehicle_id]
       
            

        
        #dimensão, linha e coluna
    solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added
    #print(position)
    #print(solution.route_vertices[4, vehicle_type_index, vehicle_id])
    #.route_vertex_cnt(vehicle_type_index, vehicle_id) = .route_vertex_cnt(vehicle_type_index, vehicle_id) + 1

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1

    if vertex_list.vertices[vertex_to_be_added].mandatory == 1:
        #solution.net_profit = solution.net_profit + penalty
        solution.net_profit = solution.net_profit + penalty
    
    return solution



def Remove(solution, vehicle_type_index, vehicle_id, position,  penalty):

    vertex_to_removed = solution.route_vertices[position, vehicle_type_index, vehicle_id]

    solution.vertices_visited[vertex_to_removed] = solution.vertices_visited[vertex_to_removed] -1

    for i in range(position, solution.route_vertex_cnt[vehicle_type_index, vehicle_id] - 1): #perguntar
        #print("position", position, "vertice", vertice)
        solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i+1, vehicle_type_index, vehicle_id]

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] = solution.route_vertex_cnt[vehicle_type_index, vehicle_id] - 1

    if vertex_list.vertices[vertex_to_removed].mandatory == 1:
        solution.net_profit = solution.net_profit - penalty

    return solution