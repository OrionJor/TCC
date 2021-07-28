from Bases_base import *
from In_solution import *
from Get_m import *
from Improve_Solution import *
from Flesibility import *
from test import *
from datetime import datetime
from random import randint
import random
import gc #limpar memória


#valores = 0 -> tipo long ou seja inteiro

def VRP_Solver():

    '''
        criar as váriaveis
    '''
    reply = None #Recebe o resultdo da interação das funções

    Compat_vehicle = load_workbook(filename = "Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm", read_only=True)   # open an Excel file and return a workbook

    # Se exite as tabelas e se estão povoadas 1,2,3 a interface da planinha controla isso
    if '1.Locations' in Compat_vehicle.sheetnames and '2.Distances' in Compat_vehicle.sheetnames and '3.Vehicles' in Compat_vehicle.sheetnames  and '4.Solution' in Compat_vehicle.sheetnames:
        print("Planilhas 1.Locais, 2.Distâncias, 3.Veículos e 4. A solução deve existir para que o VRP Spreadsheet Solver funcione. Para o VRP Solver")
    else:
        ## resporta para o usuário vai demorar, e pega os dados da tabela  ex.60sec de tempo da CPU, tabela Worksheets ThisWorkbook.Worksheets("VRP Solver Console").Cells(24, 3).value
        print("Isso vai demorar algums seconds.")
        #print(solver_options.CPU_time_limit)

    #Alocar mémoria e obter os dados seguintes funções
    #GetInstanceData()
    #GetVertexData()
    #GetArcData()
    #GetVehicleTypeData()
    #GetSolverOptions()

    # cria os objetos  swap_candidate -> troca dos valores candidatos
    # ReDim cria static array com elementos da lista vertex_list.num_customers -> número de clientes

    candidate_list = Candidate()

    for i in range(0, vertex_list.num_customers):
        #Atributos: mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position
        candidate_list.create_candidate(0, 0, 0, 0, -1, -1, -1)

    swap_candidate = None # Do tipo Candidate()
    #cria váriaveis tipo Inteiro long
    candidate_count = 0
    final_candidate_count = 0

    referece = 0


    #Cria objeto Solução candidate
    #incumbent = Solution_Data()

    #usa o objeto incumbent -> resultado candida
    incumbent = InitializeSolution()
    EvaluateSolution(incumbent)


    #Cria objeto best_known -> melhor resultado conhecido
    #best_known = Solution_Data()
    best_known = InitializeSolution()
    best_known = incumbent
    
    #cria as variáveis
    iteration = None #->valor de interações

    #cria a variáveis da matriz
    #observação i->origem, j -> destino, k-> veículo ou seja i-> arco atual, j -> arco posterior

    
    i = 0
    j = 0
    k = 0
    l = 0

    #cria os vetores de vértes e swap
    vertex = 0 #->tipo inteiro
    vertex_to_swap = 0 #->tipo inteiro

    #criar o vetor, vetor para swap, adicionar o tipo de veículo, id veículo e a posição
    vertex_to_be_added = 0 #-> tipo inteiro
    vehicle_type_to_add_to = 0
    vehicle_id_to_add_to = 0
    position_to_add_to = 0

    #cria max_net_profit - > maximo proximo lucro, min_total_distance -> min total de distancia,
    # max_mandatory -> maximo obrigatoria, max_secondary_profit -> maximo lucro segundario

    max_net_profit = 0 #tipo double
    min_total_distance = 0 #tipo double
    max_mandatory = 0    #tipo int
    max_secondary_profit = 0 #tipo double

    #cirar cluster_core -> número de cluster, distance_to_farthest_customer -> distância para o cliente mais distânte,
    #cluster_diameter -> diâmetro do cluter, capacity_used -> capacidade usada
    cluster_core = -1 #tipo inteiro
    distance_to_farthest_customer = 0 #tipo double
    cluster_diameter = 0 #tipo double
    capacity_used = -1 #tipo dolble

    #cria removal_rate -> taxa de remoção, insertion_heuristic -> heurística de inserção
    removal_rate = 0 #tipo double
    insertion_heuristic = 0 #tipo double

    #cria start_time -> hora de início, end_tipo -> hora de fim, time_elapsed -> tempo percorrido

    start_time = 0 #tipo date
    end_time = 0 #tipo date
    time_elapsed = 0 #tipo double


    #infeasibility check -> verificar de inviabilidade com o contador e com string 
    infeasibility_count = 0 #tipo inteiro
    infeasibility_string =""

    FeasibilityCheckData(infeasibility_count, infeasibility_string)

    if infeasibility_count > 0:
        reply = "Razões para inviabilidade detectadas. " + infeasibility_string + " Deseja continuar? " + " VRP Solucionador de planilhas"
        #print(reply)


    #read best known solution -> leia a solução a mais conhecida
    #começo quente == true, entação a funções (ReadSolution e EvaluateSolution) -> com o objeto de incumbet


    if solver_options.warm_start == True:
    
        ReadSolution(incumbent)
        EvaluateSolution(incumbent)

        #se objeto incumbente.feasible == true, o melhor resultado viável conhecido receobe o objeto best_known == incumbent
        if incumbent.feasible == True:
            best_known = incumbent
    
    #pega o tempo de CPU
    start_time = datetime.now() #-> tempo inicial de execução no computador
    end_time = datetime.now() #-> tempo final de execução no computador
    
    #constructive plase - > "faze construtiva mostra na tela para o usuário esperar"
    #if solver_options.status_updates == True:
        #print("Contruindo Solução Por Favor Espere .....")

    #print(best_known.route_vertices)
    DeterminePenalty(instance)

    EvaluateSolution(incumbent)

    if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
        (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
        (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):
        
        #((titular viável = Verdadeiro) E (mais conhecido. viável = Falso)) Ou
        #((titular cobre vértices obrigatórios = Verdadeiro) E (mais conhecido cobre vértices obrigatórios = Falso)) Ou
        #((histórico viável = mais conhecido viável) E (lucro líquido histórico> lucro líquido mais conhecido + epsilon

        best_known = incumbent

    if abs(best_known.net_profit - incumbent.net_profit) > epsilon:
        ImproveSolution(best_known, instance.penalty)
        ImproveSolution(incumbent, instance.penalty)
    
    else:
        ImproveSolution(best_known, instance.penalty)


    if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
        (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
        (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):

        best_known = incumbent

    incumbent = InitializeSolution()#chama a função InitializeSolution

    #For i = 1 To vehicle_type_list.num_vehicle_types
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable): #número de veiculos
            #tipo de veículo list.tipos_veículos (in). número disponível
            #Criar o cluster
            cluster_core = -1
            capacity_used = 0

            distance_to_farthest_customer = 0
            #distância para o cliente mais distante
            #For k = vertex_list.num_depots + 1 To vertex_list.num_locations
            for k in range(vertex_list.num_depots, vertex_list.num_locations):
                #arc_list.distance -> é um vetor.
                if(arc_list.distance[vehicle_type_list.vehicle_types[i].OriginBaseId, k] + arc_list.distance[k, vehicle_type_list.vehicle_types[i].ReturnBaseId] > cluster_diameter) and (vertex_list.vertices[k].mandatory >= 0) and (incumbent.vertices_visited[k] == 0):
                    distance_to_farthest_customer = arc_list.distance[vehicle_type_list.vehicle_types[i].OriginBaseId, k] + arc_list.distance[k, vehicle_type_list.vehicle_types[i].ReturnBaseId]
                    cluster_core = k
            
            if cluster_core != -1:
                #AddVertex(incumbent, cluster_core, i, j, 1)# anterior
                AddVertex(incumbent, cluster_core, i, j, 0, instance.penalty)
                capacity_used =  abs(vertex_list.vertices[cluster_core].PickupAmount + vertex_list.vertices[cluster_core].DeliveryAmount)


                while True:

                    vertex_to_be_added = -1
                    cluster_diameter = (arc_list.distance[vehicle_type_list.vehicle_types[i].OriginBaseId, cluster_core] + arc_list.distance[cluster_core, vehicle_type_list.vehicle_types[i].ReturnBaseId]) / 2

                    #For k = vertex_list.num_depots + 1 To vertex_list.num_locations
                    for k in range(vertex_list.num_depots, vertex_list.num_locations):

                        if(arc_list.distance[cluster_core, k] + arc_list.distance[k, cluster_core] < cluster_diameter) and (capacity_used + vertex_list.vertices[k].PickupAmount <= vehicle_type_list.vehicle_types[i].capacity) and (vertex_list.vertices[k].mandatory >= 0) and (incumbent.vertices_visited[k] == 0):
                            
                            cluster_diameter = arc_list.distance[cluster_core, k] + arc_list.distance[k, cluster_core]
                            vertex_to_be_added = k

                        if vertex_to_be_added != -1:
                            #AddVertex(incumbent, vertex_to_be_added, i, j, incumbent.route_vertex_cnt[i, j] + 1) anterior
                            AddVertex(incumbent, vertex_to_be_added, i, j, incumbent.route_vertex_cnt[i, j], instance.penalty)
                            capacity_used = capacity_used + vertex_list.vertices[vertex_to_be_added].PickupAmount

                    #Do while
                    if vertex_to_be_added == -1:
                        break
                
                ImproveSolution(incumbent, instance.penalty)
    
    while True:

        vertex_to_be_added = -1 # número de vertice -> adicionado
        #DeterminePenalty(instance)
        
        if instance.penalty == 0:
            DeterminePenalty(instance)
        
        max_net_profit = incumbent.net_profit - instance.penalty #max de lucro - visitas
        min_total_distance = incumbent.total_distance # total min de distância
        max_mandatory = 0 # número maximo de vistas obrigatorias
        #print(incumbent.net_profit)
        #segundo loop número de depositos +1 até o número de locais
        #vertex -> é uma posição


        for vertex2 in range(vertex_list.num_depots, vertex_list.num_locations):
            #vertex_list.vertices-> dados obtidos dos métodos GetVexdata, GetArcData, GetVeicle, GetSolver
            
 
            if(vertex_list.vertices[vertex2].mandatory >= 0) and (incumbent.vertices_visited[vertex2] == 0): #incumbent.vertices_visited[vertex] não tem nada

                #For i = 1 To vehicle_type_list.num_vehicle_types
                for si in range(0, vehicle_type_list.num_vehicle_types):
                    #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
                    for sj in range(0, vehicle_type_list.vehicle_types[si].NumberAvailable):
                        if sj == 0:

                            #vetor de nos com oirigem e destino
                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for sk in range(0, incumbent.route_vertex_cnt[si, sj] +1):
                                #adiciona o vetor e chama a função
                                AddVertex(incumbent, vertex, si, sj, sk, instance.penalty)

                                if(vertex_list.vertices[vertex2].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex2].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex2].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex2].mandatory
                                    vertex_to_be_added = vertex2
                                    vehicle_type_to_add_to = si
                                    vehicle_id_to_add_to = sj
                                    position_to_add_to = sk

                                RemoveVertex(incumbent, si, sj, sk, instance.penalty)
                        elif incumbent.route_vertex_cnt[si, sj -1] > 0:

                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[si, sj] + 1):
                                
                                AddVertex(incumbent, vertex, si, sj, sk, instance.penalty)

                                if(vertex_list.vertices[vertex2].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex2].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex2].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex2].mandatory
                                    vertex_to_be_added = vertex2
                                    vehicle_type_to_add_to = si
                                    vehicle_id_to_add_to = sj
                                    position_to_add_to = sk

                                RemoveVertex(incumbent, si, sj, sk, instance.penalty)

        
        if vertex_to_be_added != -1:
            #AddVertex(incumbent, vertex_to_be_added, vehicle_type_to_add_to, vehicle_id_to_add_to, position_to_add_to)
            AddVertex(incumbent, vertex_to_be_added, vehicle_type_to_add_to, vehicle_id_to_add_to, position_to_add_to, instance.penalty)

            #end_time = Now
            #print "Added vertex: " & vertex_to_be_added & " obj: " & incumbent.net_profit
            
            #hora final = agora
            #print "vértice adicionado:" & vértice a ser adicionado & "obj:" & lucro líquido incumbente
        EvaluateSolution(incumbent)

        if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
            (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
            (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):
        
            #((titular viável = Verdadeiro) E (mais conhecido. viável = Falso)) Ou
            #((titular cobre vértices obrigatórios = Verdadeiro) E (mais conhecido cobre vértices obrigatórios = Falso)) Ou
            #((histórico viável = mais conhecido viável) E (lucro líquido histórico> lucro líquido mais conhecido + epsilon

            best_known = incumbent

                        
        if vertex_to_be_added == -1:
            break

    #https://stackoverflow.com/questions/1316767/how-can-i-explicitly-free-memory-in-python
    #Erase the data
    #Free na memória e ensera as funções

    #del vertex_list.vertices
    #del arc_list.distance
    #del arc_list.duration
    #del vehicle_type_list.vehicle_types

    #del incumbent

    #del best_known
    
    #gc.collect()
    
    
    
    '''
    for i in range(0, vehicle_type_list.num_vehicle_types):
        #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
        for j in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
            print("route_vertex_cnt", incumbent.route_vertex_cnt[i,j])
    '''
    '''
    for vet in range(vertex_list.num_depots, vertex_list.num_customers):
        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
            for j in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
                print("vertex", incumbent.route_vertices[vet, i, j])
    
    #print(incumbent.net_profit)
    '''
    #print(best_known.route_vertices)

    for i in range(0, vehicle_type_list.num_vehicle_types):
        #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
        for j in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
            for k in range(0, incumbent.route_vertex_cnt[i,j]):
                print(incumbent.route_vertices[k, i, j])
VRP_Solver()