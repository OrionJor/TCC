from Bases_base import *
from Get_m import *

#!!!!!!!!!!Depois colocar parametro solution = Solution_Data()
def InitializeSolution():

    i = 0
    j = 0
    k = 0

    max_number_of_vehicles = 0

    # para teste depois tem que tirar !!!
    solution = Solution_Data()

    solution.feasible = False
    solution.covers_mandatory_vertices = False
    solution.net_profit = 0
    solution.total_distance = 0

    vehicle_type_list = GetVehicleTypeData()

    for  i in range(0, vehicle_type_list.num_vehicle_types):
        if max_number_of_vehicles < vehicle_type_list.vehicle_types[i].number_available:
            max_number_of_vehicles = vehicle_type_list.vehicle_types[i].number_available
    
    vertex_list = GetVertexData()

    solution.net_profit_per_route = [[0]*max_number_of_vehicles for i in range(vehicle_type_list.num_vehicle_types)]
    solution.total_distance_per_route = [[0]*max_number_of_vehicles for i in range(vehicle_type_list.num_vehicle_types)]
    solution.route_vertex_cnt = [[0]*max_number_of_vehicles for i in range(vehicle_type_list.num_vehicle_types)]
    
    #coluna , linha , profundidade ou blocos
    #m = [[[0 for i in range(4)] for j in range(3) ] for k in range(2)]
    solution.route_vertices = [[[-1 for i in range(max_number_of_vehicles)] for j in range(vehicle_type_list.num_vehicle_types) ]for k in range(vertex_list.num_customers)]
    

    '''
    não necessario
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
            solution.net_profit_per_route[i][j] = 0
            solution.total_distance_per_route[i][j] = 0
            solution.route_vertex_cnt[i][j] = 0

            for k in range(0, vertex_list.num_customers):
                solution.route_vertex_cnt[i][j][k] = -1
    ReDim DP_list.control(1 To vertex_list.num_customers)
    ReDim DP_list.value(1 To vertex_list.num_customers)
    '''
    
    #print(solution.vertices_visited[0][2])

    return solution

#para teste
#InitializeSolution()

##!!!!!!!!!!Depois colocar parametro solution = Solution_Data()!!!!!!!!!!!
def ReadSolution():
    dados = pd.read_excel('Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm',sheet_name="4. Solução")

    i = 0
    j = 0
    k = 0

    vertex_to_be_added = 0
    
    stop_count_claimed = 0
    stop_count_realized = 0
    
    offset = 0

    # para teste depois tem que tirar !!!
    solution = InitializeSolution()

    #esse precisa
    vehicle_type_list = GetVehicleTypeData()
    
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
    
            stop_count_claimed = (dados.iloc[1,6] + offset)
            stop_count_realized = 0

            for k in range(0, stop_count_claimed):
                if  ((dados.iloc[4+k, 1 + offset] != None) and (dados.iloc[4 +k, 1 + offset] != dados.iloc[4, 1 + offset]) and (dados.iloc[4+k, 1 + offset] != vehicle_type_list.vehicle_types[i].return_base_id)):
                    #vertex_to_be_added = Cells(4 + k, 2 + offset).value + 1 -> não precisa
                    vertex_to_be_added = dados.iloc[4+k, 2 + offset]
                    print(vertex_to_be_added)
                    stop_count_realized = stop_count_realized +1
                    #chama a função 
                    AddVertex(solution, vertex_to_be_added, i, j, stop_count_realized)
                    #'MsgBox "Added vertex " & vertex_to_be_added
            
            offset = offset + offset_constant


    
    return solution



#parametro para ser colocados
#solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position


#entender no papel
def AddVertex(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position):

    #para testes depois tirar
    #solution = Solution_Data()
    #.vertices_visited(vertex_to_be_added) = .vertices_visited(vertex_to_be_added) + 1
    solution.vertices_visited[vertex_to_be_added] += 1
    
    #mudança -> 'shift
    rota_do_vértice_cnt = solution.route_vertex_cnt(vehicle_type_index, vehicle_id)

    #https://pynative.com/python-range-function/ step maior para menor
    #for i in range(6,0,-1):
    for i in range( position,rota_do_vértice_cnt, -1):
        #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i) -> perguntar
        solution.route_vertices[i+1][vehicle_type_index][vehicle_id] = solution.route_vertices[i][vehicle_type_index][vehicle_id]

    solution.route_vertices[position][vehicle_type_index][vehicle_id] = vertex_to_be_added

    #.route_vertex_cnt(vehicle_type_index, vehicle_id) = .route_vertex_cnt(vehicle_type_index, vehicle_id) + 1
    solution.route_vertex_cnt[vehicle_type_index][vehicle_id] += 1 
    

    instance = GetInstanceData()
    if  instance.multi_trip == True:
        #EvaluateRouteMultiTrip(solution, vehicle_type_index, vehicle_id)
        pass
    else:
        #EvaluateRouteSingleTrip(solution, vehicle_type_index, vehicle_id)
        pass
    
    vertex_list = GetVertexData()

    if vertex_list.vertices[vertex_to_be_added].mandatory == 1:
        solution.net_profit = solution.net_profit + instance.penalty


    return solution

    

#para teste
#AddVertex()
#ReadSolution()