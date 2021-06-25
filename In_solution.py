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

    #De onde vem os dados
    #vehicle_type_list = GetVehicleTypeData()

    for  i in range(0, vehicle_type_list.num_vehicle_types):
        if max_number_of_vehicles < vehicle_type_list.vehicle_types[i].number_available:
            max_number_of_vehicles = vehicle_type_list.vehicle_types[i].number_available
    
    #De onde vem os dados
    #vertex_list = GetVertexData()

    #linha e coluna
    solution.net_profit_per_route = np.zeros((vehicle_type_list.num_vehicle_types, max_number_of_vehicles), dtype ='int16')
    
    solution.total_distance_per_route = np.zeros(( vehicle_type_list.num_vehicle_types, max_number_of_vehicles), dtype='int16')
    solution.route_vertex_cnt = np.zeros((vehicle_type_list.num_vehicle_types, max_number_of_vehicles), dtype='int16')
    
    #coluna , linha , profundidade ou blocos modelo antigo
    #m = [[[0 for i in range(4)] for j in range(3) ] for k in range(2)]
    #solution.route_vertices = [[[-1 for i in range(max_number_of_vehicles)] for j in range(vehicle_type_list.num_vehicle_types) ]for k in range(vertex_list.num_customers)]
    
    #profundidade ou blocos, coluna e linha  modelo novo numpy
    solution.route_vertices = np.ones_like(( vertex_list.num_customers,vehicle_type_list.num_vehicle_types, max_number_of_vehicles), dtype='int32')
    solution.route_vertices[:] = -1

    solution.vertices_visited =  np.zeros((vertex_list.num_locations), dtype='int16')


    '''
    não necessario
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
            solution.net_profit_per_route[i][j] = 0
            solution.total_distance_per_route[i][j] = 0
            solution.route_vertex_cnt[i][j] = 0

            for k in range(0, vertex_list.num_customers):
                solution.route_vertex_cnt[i][j][k] = -1
    
    '''
    DP_list.control = [[] for i in range(vertex_list.num_customers)]
    DP_list.value = [[] for i in range(vertex_list.num_customers)]
    
    #print(solution.vertices_visited[0][2])
    #objeto principal
    #return solution

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

    #sabe de onde vem objeto
    #vehicle_type_list = GetVehicleTypeData()
    
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


    #saber de onde vem o objeto principal
    #return solution



#parametro para ser colocados
#solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position


#entender no papel
def AddVertex(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position):

    #para testes depois tirar
    #solution = Solution_Data()
    #.vertices_visited(vertex_to_be_added) = .vertices_visited(vertex_to_be_added) + 1
    solution.vertices_visited[vertex_to_be_added] += 1
    
    #mudança -> 'shift
    rota_do_vertice_cnt = solution.route_vertex_cnt(vehicle_type_index, vehicle_id)

    #https://pynative.com/python-range-function/ step maior para menor
    #inicio, fim, e step
    #for i in range(6,0,-1): -> temos que testar
    for i in range(rota_do_vertice_cnt, position, -1):
        #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i) -> perguntar
        solution.route_vertices[i+1, vehicle_type_index, vehicle_id] = solution.route_vertices[i + 1, vehicle_type_index, vehicle_id]

    #dimensão, linha e coluna
    solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added
    

    #.route_vertex_cnt(vehicle_type_index, vehicle_id) = .route_vertex_cnt(vehicle_type_index, vehicle_id) + 1
    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1 
    
    #saber de onde vem os dados
    #instance = GetInstanceData()
    if  instance.multi_trip == True:
        #EvaluateRouteMultiTrip(solution, vehicle_type_index, vehicle_id)
        pass
    else:
        #EvaluateRouteSingleTrip(solution, vehicle_type_index, vehicle_id)
        pass

    #saber de onde vem os dados
    #vertex_list = GetVertexData()

    if vertex_list.vertices[vertex_to_be_added].mandatory == 1:
        solution.net_profit = solution.net_profit + instance.penalty

    #objeto principal
    #return solution



def RemoveVertex(solution, vehicle_type_index, vehicle_id, position):

    #para testes depois tirar
    solution = Solution_Data()

    vertex_to_removed = 0

    vertex_to_removed = solution.route_vertices[position, vehicle_type_index, vehicle_id]

    solution.vertices_visited[vertex_to_removed] -= 1

    vertice = solution.route_vertex_cnt(vehicle_type_index, vehicle_id)
    
    for i in range(position, vertice, -1):
        solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i+1, vehicle_type_index, vehicle_id]

    solution.route_vertex_cnt[vehicle_type_index, vehicle_id] -= 1

    #saber de onde vem os dados
    #instance = GetInstanceData()

    if instance.multi_trip == True:
        #EvaluateRouteMultiTrip(solution, vehicle_type_index, vehicle_id)
        pass
    else:
        #EvaluateRouteMultiTrip(solution, vehicle_type_index, vehicle_id)
        pass

    #saber de onde vem os dados
    #vertex_list =  GetVertexData()
    if vertex_list.vertices[vertex_to_removed].mandatory == 1:
        solution.net_profit = solution.net_profit - instance.penalty


def EvaluateSolution(solution):

    i = 0
    j = 0

    #para testes depois tirar
    solution = Solution_Data()

    solution.net_profit = 0

    #saber de onde vem os dados
    #vehicle_type_list = GetVehicleTypeData()
    
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
            solution.net_profit_per_route[i,j] = 0

    solution.feasible = True
    solution.covers_mandatory_vertices = True

    #saber de onde vem os dados
    #instance = GetInstanceData()
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types(i).number_available):
            if instance.multi_trip == True:
                #EvaluateRouteMultiTrip(solution, i, j)
                pass
            else:
                #EvaluateRouteMultiTrip(solution, i, j)
                pass 

    
    #saber de onde vem os dados
    #vertex_list = GetVertexData()

    depositos = vertex_list.num_depots

    #verificar vértices e visitas obrigatórias
    for i in range(depositos, vertex_list.num_locations):

        if ((vertex_list.vertices[i].mandatory == 1 ) and (solution.vertices_visited[i] == 0)):
            solution.feasible = False
            solution.covers_mandatory_vertices = False
            solution.net_profit = solution.net_profit - instance.penalty

        if ((vertex_list.vertices[i].mandatory == -1 ) and (solution.vertices_visited[i] == 1)):
            solution.feasible = False
            solution.net_profit = solution.net_profit - instance.penalty

        if solution.vertices_visited[i] > 1:
            solution.feasible = False
            solution.net_profit = solution.net_profit - instance.penalty
        
    #saber que é objeto principal
    #return solution



    

#para teste
#AddVertex()
#RemoveVertex()
#ReadSolution()