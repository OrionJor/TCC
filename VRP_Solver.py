from Bases_base import *
from Get_m import *
from In_solution import *
from EvaluateRoute_Single_e_Multi_Trip import *
from datetime import dt


#terminal https://www.youtube.com/watch?v=D2BHH3wS0j0

#Exemplos http://excelevba.com.br/classes-em-vba/
#https://www.codegrepper.com/code-examples/python/initialize+list+of+a+class+object+python
#https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/

# tipo de dados VBA
#https://www.guru99.com/vba-arrays.html
#https://excelmacromastery.com/vba-dim/

#Candidate_Data.mandatory= 0

#valores =0 -> para Long 
#valores = 0.0 -> double

def VRP_Solver():

    '''
        cria as váriaveis
    '''
    Compat_vehicle = load_workbook(filename="Dados/VRP_Spreadsheet_Solver_correta_Modelo.xlsm", read_only=True)   # open an Excel file and return a workbook
    
    # Se exite as tabelas e se estão povoadas 1,2,3 a interface da planinha controla isso
    if '1.Locations' in Compat_vehicle.sheetnames and '2.Distances' in Compat_vehicle.sheetnames and '3.Vehicles' in Compat_vehicle.sheetnames  and '4.Solution' in Compat_vehicle.sheetnames:
        print("Planilhas 1.Locais, 2.Distâncias, 3.Veículos e 4. A solução deve existir para que o VRP Spreadsheet Solver funcione. Para o VRP Solver")
    else:
        print("Isso vai demorar algums seconds.")
        print(solver_options.CPU_time_limit)


    #Alocar memória e obter os dados
    GetInstanceData()
    GetVertexData()
    GetArcData()
    GetVehicleTypeData()
    GetSolverOptions()
    
    DeterminePenalty()


    # cria os objetos  swap_candidate -> troca dos valores candidatos
    # ReDim cria static array com elementos da lista vertex_list.num_customers -> número de clientes
    swap_candidate = Candidate_Data()

    #cria váriaveis tipo Inteiro long
    candidate_count = 0
    final_candidate_count = 0

    # Cria objeto
    incumbent = Solution_Data()

    # Call -> chama funções
    #Usa o objetos incumbent -> resultado candidata.
    InitializeSolution(incumbent)
    EvaluateSolution(incumbent)
    #print(incumbent.feasible)

    # cria o objeto best_known ->  melhor resultado conhecida
    best_known = Solution_Data()

    #Chama a função InitializeSolution com parametro best_known
    InitializeSolution(best_known)

    #best_known -> recebe dados incumbent depois das funções InitializeSolution(incumbent) e EvaluateSolution(incumbent)
    best_known = incumbent
    

    #cria as variáveis
    iteration = 0

    # cria a variáveis da matriz
    # observação i-> origem, j-> destino, k-> veiculo ou seja i->arco atual, j ->arco posterior
    i = 0
    j = 0
    k = 0
    l = 0

    #cria o vetor e vetor para swap para as troca de possições de vetores
    vertex = 0
    vertex_to_swap = 0


    #cria o vetor, vetor para swap, adicionar o tipo de veículo, adicionar o id de veículo e posição para adicionar
    vertex_to_be_added = 0
    vehicle_type_to_add_to = 0
    vehicle_id_to_add_to = 0
    position_to_add_to = 0

    # cria max_net_profit -> maximo proximo lucro, min_total_distance -> min total de distancia,
    # max_mandatory -> maximo obrigatoria, max_secondary_profit -> max lucro segundario
    max_net_profit = 0.0
    min_total_distance = 0.0
    max_mandatory = 0
    max_secondary_profit = 0

    # cria cluster_core -> número de cluster, distance_to_farthest_customer -> distância para o cliente mais distânte, 
    #cluster_diameter -> diâmetro do cluster, capacity_used -> capacidade usada  
    cluster_core = 0
    distance_to_farthest_customer = 0.0
    cluster_diameter = 0.0
    capacity_used = 0.0

    # cria start_time -> hora de início, end_time -> hora de fim, time_elapsed -> tempo pecorrido
    start_time = 0
    end_time = 0
    time_elapsed = 0.0

    #infeasibility check -> verificação de inviabilidade conta e string
    
    infeasibility_count = 0
    infeasibility_string =""

    #infeasibility_count = FeasibilityCheckData(infeasibility_count, infeasibility_string)
    
    # mosta na tela a inviabilidade
    if infeasibility_count > 0:
        print("Razões de inviabilidade detectadas.")


    if solver_options.warm_start == True:
        ReadSolution(incumbent)
        EvaluateSolution(incumbent)

        if incumbent.feasible == True:
            best_known = incumbent
    
    #outra forma de medir o tempo de execução da CPU com a time()
    #https://pt.stackoverflow.com/questions/97364/medir-o-tempo-de-execu%C3%A7%C3%A3o-de-uma-fun%C3%A7%C3%A3o 
    start_time = dt.datetime.now()
    end_time = dt.datetime.now()

    if solver_options.status_updates == True:
        print("contruindo Solução Espere")


    # não tem Do while em python tutorial https://www.javatpoint.com/python-do-while-loop 
    while True:
        vertex_to_be_added = -1 #  número de vertice-> adicionado
        max_net_profit = incumbent.net_profit - instance.penalty # max de lucros lucro - visitas
        min_total_distance = incumbent.total_distance # total min de distância
        max_mandatory = 0
        
        if (vertex_to_be_added != -1 ):
            break