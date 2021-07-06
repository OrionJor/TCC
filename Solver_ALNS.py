from Bases_base import *
from In_solution import *
from Get_m import *
from Improve_Solution import *
from Flesibility import *
from EvaluateRoute_Single_e_Multi_Trip import *
from datetime import datetime
from random import randrange, randint
import random



#valores = 0 -> tipo long ou seja inteiro

def VRP_Solver():

    '''
        criar as váriaveis
    '''
    reply = None #Recebe o resultdo da interação das funções

    Compat_vehicle = load_workbook(filename = " Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm", read_only=True)   # open an Excel file and return a workbook

    # Se exite as tabelas e se estão povoadas 1,2,3 a interface da planinha controla isso
    if '1.Locations' in Compat_vehicle.sheetnames and '2.Distances' in Compat_vehicle.sheetnames and '3.Vehicles' in Compat_vehicle.sheetnames  and '4.Solution' in Compat_vehicle.sheetnames:
        print("Planilhas 1.Locais, 2.Distâncias, 3.Veículos e 4. A solução deve existir para que o VRP Spreadsheet Solver funcione. Para o VRP Solver")
    else:
        ## resporta para o usuário vai demorar, e pega os dados da tabela  ex.60sec de tempo da CPU, tabela Worksheets ThisWorkbook.Worksheets("VRP Solver Console").Cells(24, 3).value
        print("Isso vai demorar algums seconds.")
        #print(solver_options.CPU_time_limit)

    #Alocar mémoria e obter os dados

    GetInstanceData()
    GetVertexData()
    GetArcData()
    GetVehicleTypeData()
    GetSolverOptions()

    DeterminePenalty()

    # cria os objetos  swap_candidate -> troca dos valores candidatos
    # ReDim cria static array com elementos da lista vertex_list.num_customers -> número de clientes

    candidate_list = Candidate()

    for i in range(0, vertex_list.num_customers):
        #Atributos: mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position
        candidate_list.create_candidate(None, None, None, None, None, None, None)

    swap_candidate = None # Do tipo Candidate()
    #cria váriaveis tipo Inteiro long
    candidate_count = 0
    final_candidate_count = 0


    #Cria objeto Solução candidate
    incumbent = Solution_Data()

    #usa o objeto incumbent -> resultado candida
    InitializeSolution(incumbent)
    EvaluateSolution(incumbent)

    #Cria objeto best_known -> melhor resultado conhecido
    best_known = Solution_Data()
    
    
    #cria as variáveis
    iteration = None #->valor de interações

    #cria a variáveis da matriz
    #observação i->origem, j -> destino, k-> veículo ou seja i-> arco atual, j -> arco posterior

    
    i = 0
    j = 0
    k = 0
    l = 0

    #cria os vetores de vértes e swap
    vertex = None #->tipo inteiro
    vertex_to_swap = None #->tipo inteiro

    #criar o vetor, vetor para swap, adicionar o tipo de veículo, id veículo e a posição
    vertex_to_be_added = None #-> tipo inteiro
    vehicle_type_to_add_to = None
    vehicle_id_to_add = None
    positon_to_add_to = None

    #cria max_net_profit - > maximo proximo lucro, min_total_distance -> min total de distancia,
    # max_mandatory -> maximo obrigatoria, max_secondary_profit -> maximo lucro segundario

    max_net_profit = None #tipo double
    min_total_distance = None #tipo double
    max_mandatory = None    #tipo int
    max_secondary_profit = None #tipo double

    #cirar cluster_core -> número de cluster, distance_to_farthest_customer -> distância para o cliente mais distânte,
    #cluster_diameter -> diâmetro do cluter, capacity_used -> capacidade usada
    cluster_core = None #tipo inteiro
    distance_to_farthest_customer = None #tipo double
    cluster_diameter = None #tipo double
    capacity_used = None #tipo dolble

    #cria removal_rate -> taxa de remoção, insertion_heuristic -> heurística de inserção
    removal_rate = None #tipo double
    insertion_heuristic = None #tipo double

    #cria start_time -> hora de início, end_tipo -> hora de fim, time_elapsed -> tempo percorrido

    start_time = None #tipo date
    end_time = None #tipo date
    time_elapsed = None #tipo double


    #infeasibility check -> verificar de inviabilidade com o contador e com string 
    infeasibility_count = None #tipo inteiro
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
    if solver_options.status_updates == True:
        print("Contruindo Solução Por Favor Espere .....")

    while True:

        vehicle_id_to_add = -1 # número de vertice -> adicionado
        max_net_profit = incumbent.net_profit - instance.penalty #max de lucro - visitas
        min_total_distance = incumbent.total_distance # total min de distância
        max_mandatory = 0 # número maximo de vistas obrigatorias

        #segundo loop número de depositos +1 até o número de locais
        #vertex -> é uma posição

        #For vertex = vertex_list.num_depots + 1 To vertex_list.num_locations
        for vertex in range(vertex_list.num_depots, vertex_list.num_locations):
            #vertex_list.vertices-> dados obtidos dos métodos GetVexdata, GetArcData, GetVeicle, GetSolver 
            if(vertex_list.vertices[vertex] >= 0) and (incumbent.vertices_visited[vertex] == 0): #incumbent.vertices_visited[vertex] não tem nada

                #For i = 1 To vehicle_type_list.num_vehicle_types
                for i in range(0, vehicle_type_list.num_vehicle_types):
                    #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
                    for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                        if j == 0:

                            #vetor de nos com oirigem e destino
                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[i, j]):
                                #adiciona o vetor e chama a função
                                AddVertex(incumbent, vertex, i, j, k)

                                if(vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex].madatory
                                    vertex_to_be_added = vertex
                                    vehicle_type_to_add_to = i
                                    vehicle_id_to_add = j
                                    positon_to_add_to = k

                                RemoveVertex(incumbent, i, j, k)

                        elif incumbent.route_vertex_cnt[i, j -1] > 0:

                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[i, j]):
                                
                                AddVertex(incumbent, vertex, i, j, k)

                                if(vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex].madatory
                                    vertex_to_be_added = vertex
                                    vehicle_type_to_add_to = i
                                    vehicle_id_to_add = j
                                    positon_to_add_to = k

                                RemoveVertex(incumbent, i, j, k)


        if vehicle_id_to_add != -1:
            AddVertex(incumbent, vertex_to_be_added, vertex_to_be_added, positon_to_add_to)

            #end_time = Now
            #print "Added vertex: " & vertex_to_be_added & " obj: " & incumbent.net_profit
            
            #hora final = agora
            #print "vértice adicionado:" & vértice a ser adicionado & "obj:" & lucro líquido incumbente
        
        EvaluateSolution(incumbent)

        if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
            (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
            (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):

            best_known = incumbent
        
        #Do While
        if vehicle_id_to_add != -1: #se ainda tiver vetor continua -> vertex_to_be_added diferente de -1  e se não tiver para 
            break

    #se a solução conhecida do valor (lucro líquido melhor conhecida - lucro líquido incumbent > 0.0001) -> melhora a solução
    #se não só melhora a solução da melhor conhecida
    if(-1 * (best_known.net_profit - incumbent.net_profit)) > epsilon:
        ImproveSolution(best_known)
        ImproveSolution(incumbent)
    
    else:
        ImproveSolution(best_known)

    #EvaluateSolution(incumbent)
    #EvaluateSolution(incumbent)

    #Se o incumbent é a mais viável do que best_known então o best_known = incumbent
    if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
        (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
        (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):

        best_known = incumbent

    #2nd constructive heuristic
    #2ª heurística construtiva

    InitializeSolution(incumbent) #chama a função InitializeSolution

    #For i = 1 To vehicle_type_list.num_vehicle_types
    for i in range(0, vehicle_type_list.num_vehicle_types):
        for j in range(0, vehicle_type_list.num_vehicle_types[i].mumber_available): #número de veiculos
            #tipo de veículo list.tipos_veículos (in). número disponível

            cluster_core = -1
            capacity_used = 0

            distance_to_farthest_customer = 0
            #distância para o cliente mais distante
            #For k = vertex_list.num_depots + 1 To vertex_list.num_locations
            for k in range(vertex_list.num_depots, vertex_list.num_locations):
                #arc_list.distance -> é um vetor.
                if(arc_list.distance[vehicle_type_list.vehicle_types[i].origin_base_id, k] + arc_list.distance[k, vehicle_type_list.vehicle_types[i].return_base_id] > cluster_diameter) and (vertex_list.vertices[k].mandadory >= 0) and (incumbent.vertices_visited[k] == 0):
                    distance_to_farthest_customer = arc_list.distance[vehicle_type_list.vehicle_types[i].origin_base_id, k] + arc_list.distance[k, vehicle_type_list.vehicle_types[i].return_base_id]
                    cluster_core = k
            
            if cluster_core != -1:
                #AddVertex(incumbent, cluster_core, i, j, 1)# resolver essa parada
                AddVertex(incumbent, cluster_core, i, j, 1)
                capacity_used = (-1 * (vertex_list.vertices[cluster_core].pickup_amount + vertex_list.vertices[cluster_core].delivery_amount))


                while True:

                    vertex_to_be_added = -1
                    cluster_diameter = (arc_list.distance[vehicle_type_list.vehicle_types[i].origin_base_id, cluster_core] + arc_list.distance[cluster_core, vehicle_type_list.vehicle_types[i].return_base_id]) / 2

                    #For k = vertex_list.num_depots + 1 To vertex_list.num_locations
                    for k in range(vertex_list.num_depots, vertex_list.num_locations):

                        if(arc_list.distance[cluster_core, k] + arc_list.distance[k, cluster_core] < cluster_diameter) and (capacity_used + vertex_list.vertices[k].pickup_amount <= vehicle_type_list.vehicle_types[i].capacity) and (vertex_list.vertices[k].mandatory >= 0) and (incumbent.vertices_visited[k] == 0):
                            
                            cluster_diameter = arc_list.distance[cluster_core, k] + arc_list.distance[k, cluster_core]
                            vertex_to_be_added = k

                        if vertex_to_be_added != -1:
                            #AddVertex(incumbent, vertex_to_be_added, i, j, incumbent.route_vertex_cnt[i, j] + 1) resolver essa parada
                            AddVertex(incumbent, vertex_to_be_added, i, j, incumbent.route_vertex_cnt[i, j])
                            capacity_used = capacity_used + vertex_list.vertices[vertex_to_be_added].pickup_amount

                    #Do while
                    if vertex_to_be_added != -1:
                        break
                
                ImproveSolution(incumbent)

    while True:
        
        vehicle_id_to_add = -1
        max_net_profit = incumbent.net_profit - instance.penalty
        min_total_distance = incumbent.total_distance
        max_mandatory = 0
        
        #segundo loop número de depositos +1 até o número de locais
        #vertex -> é uma possição
        #For vertex = vertex_list.num_depots + 1 To vertex_list.num_locations
        
        for vertex in range(vertex_list.num_depots, vertex_list.num_locations):
            if (vertex_list.vertices[vertex].mandatory >= 0) and (incumbent.vertices_visited[vertex] == 0):

                #For i = 1 To vehicle_type_list.num_vehicle_types
                for i in range(0, vehicle_type_list.num_vehicle_types):
                    #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
                    for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                        if j == 0:

                            #vetor de nos com oirigem e destino
                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[i, j]):
                                #adiciona o vetor e chama a função
                                AddVertex(incumbent, vertex, i, j, k)

                                if(vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex].madatory
                                    vertex_to_be_added = vertex
                                    vehicle_type_to_add_to = i
                                    vehicle_id_to_add = j
                                    positon_to_add_to = k

                                RemoveVertex(incumbent, i, j, k)

                        elif incumbent.route_vertex_cnt[i, j -1] > 0:

                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[i, j]):
                                
                                AddVertex(incumbent, vertex, i, j, k)

                                if(vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex].madatory
                                    vertex_to_be_added = vertex
                                    vehicle_type_to_add_to = i
                                    vehicle_id_to_add = j
                                    positon_to_add_to = k

                                RemoveVertex(incumbent, i, j, k)


        if vehicle_id_to_add != -1:
            AddVertex(incumbent, vertex_to_be_added, vertex_to_be_added, positon_to_add_to)

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
        
        #Do While
        if vehicle_id_to_add != -1: #se ainda tiver vetor continua -> vertex_to_be_added diferente de -1  e se não tiver para 
            break

    ImproveSolution(incumbent)
        
    #Se o incumbent é a mais viável do que best_known então o best_known = incumbent
    if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
        (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
        (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):

        best_known = incumbent

    else:
        incumbent = best_known

    #improvement phase
    #fase de melhoria

    print("LNS algorithm running...")

    iteration = 0

    while True:

        if solver_options.status_updates == True:
            print("Starting LNS iteration ",  iteration, ". Best total net profit so far: ", best_known.net_profit)

        #https://docs.python.org/pt-br/3.7/library/random.html ->Funções para inteiros random.randrange
        #https://pynative.com/python-random-randrange/
        #https://pense-python.caravela.club/13-estudo-de-caso-selecao-de-estrutura-de-dados/02-numeros-aleatorios.html
        removal_rate = solver_options.LNS_minimum_removal_rate + (randrange(solver_options.LNS_maximum_removal_rate, solver_options.LNS_minimum_removal_rate, -1))

        #removal_rate = solver_options.LNS_minimum_removal_rate + (((time_elapsed) / solver_options.CPU_time_limit) * (solver_options.LNS_maximum_removal_rate - solver_options.LNS_minimum_removal_rate))
        #taxa de remoção = opções do solucionador. Taxa mínima de remoção do LNS + (((tempo decorrido) / opções do solucionador. Limite de tempo da CPU) * (opções do solucionador. Taxa máxima de remoção do LNS - opções do solucionador. Taxa mínima de remoção do LNS))

        #randomly remove vertices -> remover vértices aleatoriamente

        #For i = 1 To vehicle_type_list.num_vehicle_types
        for i in range(0, vehicle_type_list.num_vehicle_types):
            #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
            for j in range(vehicle_type_list.vehicle_types[i].number_available):
                #For k = 1 To incumbent.route_vertex_cnt(i, j)
                for k in range(0, incumbent.route_vertex_cnt[i, j]):
                    
                    if k <= incumbent.route_vertex_cnt[i, j]:
                        
                        random_removal_rate = random.random() #taxa_aleatoria_remoção entre 0 e 1
                        if random_removal_rate < removal_rate:

                            RemoveVertex(incumbent, i, j, k)


        #print "Starting objective: " & incumbent.net_profit & " " & iteration
        #print "Objetivo inicial:" e lucro líquido incumbente e "" e iteração

        insertion_heuristic = randint(1,2)
        #Retorna um número inteiro aleatório entre os números que você especificar. Um novo número inteiro aleatório é retornado sempre que a planilha é calculada

        while True:

            candidate_count = 0

            #For vertex = vertex_list.num_depots + 1 To vertex_list.num_locations
            for vertex in range(vertex_list.num_depots, vertex_list.num_locations):

                if (vertex_list.vertices[vertex].mandatory >= 0) and (incumbent.vertices_visited[vertex] == 0):

                    max_mandatory = 0
                    max_net_profit = incumbent.net_profit - instance.penalty
                    vehicle_id_to_add = -1

                    #vetor de nos com oirigem e destino
                    #For i = 1 To vehicle_type_list.num_vehicle_types
                    for i in range(0, vehicle_type_list.num_vehicle_types):
                        #For j = 1 To vehicle_type_list.vehicle_types(i).number_available
                        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
                            #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                            for k in range(0, incumbent.route_vertex_cnt[i, j]):
                                
                                #adiciona o vetor e chama a função
                                AddVertex(incumbent, vertex, i, j, k)

                                if(vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                                    (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                                    max_secondary_profit = max_net_profit
                                    max_net_profit = incumbent.net_profit
                                    min_total_distance = incumbent.total_distance
                                    max_mandatory = vertex_list.vertices[vertex].mandatory
                                    vertex_to_be_added = vertex
                                    vehicle_type_to_add_to = i
                                    vehicle_id_to_add = j
                                    positon_to_add_to = k

                                elif ((vertex_list.vertices[vertex].mandatory == max_mandatory) and (incumbent.net_profit > max_secondary_profit + epsilon)):

                                    max_net_profit = incumbent.net_profit
                                
                                RemoveVertex(incumbent, i, j, k)
                            
                    
                    if vehicle_id_to_add != -1:
                        candidate_count = candidate_count + 1

                        if insertion_heuristic == 2 or max_mandatory == 0:
                            candidate_list[candidate_count].net_profit = (-1 * (max_secondary_profit - max_net_profit))
                        
                        else:
                            candidate_list[candidate_count].net_profit = max_net_profit

                        candidate_list[candidate_count].total_distance = min_total_distance
                        candidate_list[candidate_count].mandatory = max_mandatory
                        candidate_list[candidate_count].vertex_to_be_added = vertex
                        candidate_list[candidate_count].vehicle_type_index = vehicle_type_to_add_to
                        candidate_list[candidate_count].vehicle_id = vehicle_type_to_add_to
                        candidate_list[candidate_count].position = positon_to_add_to


            if candidate_count > 0:

                final_candidate_count = solver_options.LNS_candidate_list_size

                if final_candidate_count > candidate_count:
                    final_candidate_count = candidate_count

                #For i = 1 To final_candidate_count
                for i in range(0, final_candidate_count):
                    k = -1
                    max_mandatory = candidate_count[i].mandatory
                    max_net_profit = candidate_list[i].net_profit
                    min_total_distance = candidate_list[i].total_distance
                    #For j = i + 1 To candidate_count
                    for j in range(i, candidate_count):
                        if(candidate_list[j].mandatory > max_mandatory) or (
                            (candidate_list[j].mandatory >= max_mandatory) and (candidate_list[j].net_profit > max_net_profit + epsilon)) or (
                            (candidate_list[j].mandatory >= max_mandatory) and (candidate_list[j].net_profit > max_net_profit - epsilon) and (candidate_list[j].total_distance < min_total_distance - epsilon)):

                            max_mandatory = candidate_list[j].mandatory
                            max_net_profit = candidate_list[j].net_profit
                            min_total_distance = candidate_list[j].total_distance

                            k = j

                    
                    if k > - 1:
                        swap_candidate = candidate_list[i]
                        candidate_list[i] = candidate_list[k]
                        candidate_list[k] = swap_candidate

                k = randint(1, final_candidate_count)
                
                vertex_to_be_added = candidate_list[k].vertex_to_be_addeb
                vehicle_type_to_add_to = candidate_list[k].vehicle_type_index
                vehicle_id_to_add = candidate_list[k].vehicle_id
                positon_to_add_to = candidate_list[k].position

                AddVertex(incumbent, vertex_to_be_added, vehicle_type_to_add_to, vehicle_type_to_add_to, positon_to_add_to)

            
            EvaluateSolution(incumbent)
            
            if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
                (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
                (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)) or ( 
                (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit - epsilon) and (incumbent.total_distance < best_known.total_distance - epsilon)):

                #ImproveSolution(incumbent)
                best_known = incumbent

            #Do While2
            if candidate_count > 0:
                break

        #print "Before polishing: " & incumbent.net_profit & " " & incumbent.feasible & " " & iteration

        ImproveSolution(incumbent)

        #MsgBox "After polishing: " & incumbent.net_profit & " " & incumbent.feasible & " " & iteration

        end_time = datetime.now()

        time_elapsed = 86400 *(end_time - start_time)

        if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
            (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
            (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)) or ( 
            (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit - epsilon) and (incumbent.total_distance < best_known.total_distance - epsilon)):

            #ImproveSolution(incumbent)
            best_known = incumbent


        elif incumbent.net_profit < best_known.net_profit - 0.1 * (1 - (time_elapsed / solver_options.CPU_time_limit)) * (-1 *(best_known.net_profit)): #If random() < 0.5 Then

            incumbent = best_known
            EvaluateSolution(incumbent)

            
        iteration = iteration + 1

        if time_elapsed < solver_options.CPU_time_limit:
            break

        #print "Iterations performed: " & iteration


    #Solver_ALNS_finiah
    #squeeze the solution # aperte a solução

    #For i = 1 To vehicle_type_list.num_vehicle_types
    for i in range(0, vehicle_type_list.num_vehicle_types):
        #For j = 1 To vehicle_type_list.vehicle_types(i).number_available - 1
        for j in range(0, vehicle_type_list.vehicle_types[i].number_available):
            if best_known.route_vertex_cnt[i, j] == 0:
                #look for a vehicle that is used

                l = -1
                k = j + 1

                while True:

                    if best_known.route_vertex_cnt[i, j] > 0:
                        l = k

                    k = k +1

                    if (l == -1) and (k <= vehicle_type_list.vehicle_types[i].number_available):
                        break

                if l != -1:
                    best_known.route_vertex_cnt[i, j] = best_known.route_vertex_cnt[i, l]
                    #For k = 1 To best_known.route_vertex_cnt(i, l)
                    for k in range(0, best_known.route_vertex_cnt[i, j]):
                        best_known.route_vertices[k, i, j] = best_known.route_vertices[k, i, l]

                    best_known.route_vertex_cnt[i, l] = 0

    EvaluateSolution(best_known)

    #write the solution

    #print best_known.net_profit

    if best_known.feasible == True:
        reply = "Solver_ALNS executado" +  str(iteration) + " Iterações LNS e encontrou uma solução com um lucro líquido de " + str(best_known.net_profit) + ".Quer substituir a solução atual pela melhor solução encontrada?" + "Solver_ALNS"
        #WriteSolution(best_known)

    else:
        reply = "A melhor solução encontrada depois" +  str(iteration) + " As iterações LNS não satisfazem todas as restrições. Quer substituir a solução atual pela melhor solução encontrada?" + "VRP Spreadsheet Solver"

        #WriteSolution(best_known)