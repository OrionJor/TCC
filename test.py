'''
def a():
   global b
   b = "teste"
   b = 10

a()

b = 100
print(b)
''' 
def tes():
    
   global a 
   a = 0
   #a = 1
   if a == 0:
      t()
      t()
      t()
   
   print(a)

def t():

   global a 
   a = 0
   a = 2


tes()

from Bases_base import *
from In_solution import *
from Get_m import *
from ImproveSolution import *
from Flesibility import *
from EvaluateRoute_Single_e_Multi_Trip import *
from datetime import datetime



#valores = 0 -> tipo long ou seja inteiro

def VRP_Solver():

   '''
      criar as váriaveis
   '''

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

   swap_candidate = Candidate()


   for i in range(0, vertex_list.num_customers):
      #Atributos: mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position
      swap_candidate.create_candidate(None, None, None, None, None, None, None)

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

   #Usa parametro best_known
   InitializeSolution(best_known)


   #best_known -> recebe dados incumbent depois de executar as funções InitializeSolution(incumbent) e EvaluateSolution(incumbent)
   best_known = incumbent

   #cria as variáveis
   iteration = 0 #-> valor de interações

   # cria a variáveis da matriz
   # observação i-> origem,  j-> destino, k-> veiculo ou seja i->arco atual, j ->arco posterior
   i = 0
   j = 0
   k = 0
   l = 0

   # cria o vetor e vetor para swap para as troca de possições de vetores
   vertex = 0
   vertex_to_swap = 0 

   #cria o vetor, vetor para swap, adicionar o tipo de veículo, adicionar o id de veículo e posição para adicionar
   vertex_to_be_added = 0
   vehicle_type_to_add_to = 0
   vehicle_id_to_add_to = 0
   position_to_add_to = 0

   #cria max_net_profit -> maximo proximo lucro, min_total_distance -> min total de distancia,
   # max_mandatory -> maximo obrigatoria, max_secondary_profit -> max lucro segundario

   max_net_profit = None #tipo Double
   min_total_distance = None #tipo Double
   max_mandatory = 0
   max_secondary_profit = None #tipo Double

   # cria cluter_core -> número de cluster, distance_to_farthest_customer -> distância para o cliente mais distânte,
   # cluster_diameter -> diâmetro do cluster, capacity_used -> capacidade usada

   cluster_core = 0
   distance_to_farthest_customer = None #tipo Double
   cluster_diameter = None
   capacity_user = None # tipo Double

   # cria Start_time -> hora de início, end_time -> hora de fim, time_elapsed -> tempo pecorrido
   start_time = None # tipo Double
   end_time = None # tipo Double
   time_elapsed = None # tipo Double

   # infeasibility check -> verificação de inviabilidade conta e string

   infeasibility_count = 0
   infeasibility_string = "" #tipo string

   #infeasibility_count = FeasibilityCheckData(infeasibility_count, infeasibility_string)
   FeasibilityCheckData(infeasibility_count, infeasibility_string)

   # mosta na tela a inviabilidade

   if infeasibility_count > 0:
      print("Razões de inviabilidade detectadas.")

   #read best known solution -> leia a solução mais conhecida
   # começo quente == true, então chama as funções (ReadSolution e EvaluateSolution) -> com o objeto de incumbent 

   if solver_options.warm_start == True:
      ReadSolution(incumbent)
      EvaluateSolution(incumbent)
      # se objeto incumbent.feasible == true, o melhor resultado viável conhecida recebe o objeto best_known == incumbent

      if incumbent.feasible == True:
         best_known = incumbent
    

   start_time = datetime.now() # hora de inicial de tempo de CPU do computador
   end_time = datetime.now() # hora final de tempo de CPU do computador

   #constructive phase -> 'fase construtiva mostra na tela para o usuário esperar por causa que esta gerando os resultados
   if solver_options.status_updates == True:
      print("contruindo Solução Espere ...")

   while True:

      vertex_to_be_added = -1 # número de vertice-> adicionado
      max_net_profit = incumbent.net_profit - instance.penalty # max de lucros lucro - visitas
      min_total_distance = incumbent.total_distance # total min de distância
      max_mandatory = 0

      # segundo loop número de depositos +1 até o número de locais 
      # vertex -> é uma possição

      #For vertex = vertex_list.num_depots + 1 To vertex_list.num_locations
      for vertex in range(vertex_list.num_depots, vertex_list.num_locations):
         # # vertex_list.vertices -> dados obtidos dos métodos GetVexdata, GetArcData, GetVeicle, GetSolver

         if(vertex_list.vertices[vertex].mandatory >= 0) and (incumbent.vertices_visited[vertex] == 0): # # incumbent.vertices_visited(vertex) não tem nada

            #  For j = 1 To vehicle_type_list.vehicle_types(i).number_available
               for j in range(0, vehicle_type_list.vehicle_types[i].number_available ): # tipo de veículo list.vehicle types (in) .number available
                  if j == 1:

                     # vetor de nos com origem e destino
                     # For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                     for k in range(0, incumbent.route_vertex_cnt[i,j]):

                        #  vetor de nos com origem e destino
                        AddVertex(incumbent, vertex, i, j, k)

                        if (vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                           (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                           (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):


                           max_net_profit = incumbent.net_profit
                           min_total_distance = incumbent.total_distance
                           max_mandatory = vertex_list.vertices[vertex].mandatory
                           vertex_to_be_added = vertex
                           vehicle_type_to_add_to = i
                           vehicle_id_to_add_to = j
                           position_to_add_to = k
                            
                        RemoveVertex(incumbent, i, j, k)

                  elif incumbent.route_vertex_cnt[i, j - 1] > 0:
                     #For k = 1 To incumbent.route_vertex_cnt(i, j) + 1
                     for k in range(0, incumbent.route_vertex_cnt[i, j]):

                        AddVertex(incumbent, vertex, i, j, k)

                        if (vertex_list.vertices[vertex].mandatory > max_mandatory) or (
                           (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit + epsilon)) or (
                           (vertex_list.vertices[vertex].mandatory >= max_mandatory) and (incumbent.net_profit > max_net_profit - epsilon) and (incumbent.total_distance < min_total_distance - epsilon)):

                           max_net_profit = incumbent.net_profit
                           min_total_distance = incumbent.total_distance
                           max_mandatory = vertex_list.vertices[vertex].mandatory
                           vertex_to_be_added = vertex
                           vehicle_type_to_add_to = i
                           vehicle_id_to_add_to = j
                           position_to_add_to = k
                            
                        RemoveVertex(incumbent, vertex, i, j, k)

        

      if vertex_to_be_added != -1:
         AddVertex(incumbent, vertex_to_be_added, vehicle_id_to_add_to, vehicle_id_to_add_to, position_to_add_to)
         #end_time = Now
         #MsgBox "Added vertex: " & vertex_to_be_added & " obj: " & incumbent.net_profit

         #hora final = agora

         #MsgBox "vértice adicionado:" & vértice a ser adicionado & "obj:" & lucro líquido incumbente

      EvaluateSolution(incumbent)

      if ((incumbent.feasible == True) and (best_known.feasible == False)) or (
         (incumbent.covers_mandatory_vertices == True) and (best_known.covers_mandatory_vertices == False)) or (
         (incumbent.feasible == best_known.feasible) and (incumbent.net_profit > best_known.net_profit + epsilon)):

         best_known = incumbent
        
      if (vertex_to_be_added != -1 ): # se ainda tiver vetor continua -> vertex_to_be_added diferente de -1  e se não tiver para
         break

         # se não só melhora a solução da melhor conhecida

   if(-1 * (best_known.net_profit - incumbent.net_profit)) > epsilon:
      ImproveSolution(best_known)
      ImproveSolution(incumbent)
    
   else:
      ImproveSolution(best_known)