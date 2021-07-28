from Bases_base import *
from Improve_Solution2 import *
from AddVertex3_e_Remove3 import *
from Get_m import *


def RemoveVertex2(solution, vehicle_type_index, vehicle_id, position,  penalty):

   cnt = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]

   for iR in range(position, cnt-1):
      print(iR)

   solution.route_vertex_cnt[vehicle_type_index, vehicle_id] = solution.route_vertex_cnt[vehicle_type_index, vehicle_id] - 1

   return solution

def AddVertex2(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position, penalty):


    
   #solution.vertices_visited[vertex_to_be_added] += 1

   #print(solution.vertices_visited[vertex_to_be_added])
    
   #mudança -> 'shift
   #rota_do_vertice_cnt = solution.route_vertex_cnt[vehicle_type_index, vehicle_id]
   #print(position)
    
   #https://pynative.com/python-range-function/ step maior para menor
    #inicio, fim, e step
    #for i in range(6, -1, -1): -> temos que testar
    #print(rota_do_vertice_cnt)

   #Sistema para começar da posição 1 e não da 0
   #print(position-1)
   #print(position)
   #for i in range(rota_do_vertice_cnt, position, -1):#perguntar
      #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i) -> perguntar
      #solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i-1, vehicle_type_index, vehicle_id]
            

        
      #dimensão, linha e coluna
   #solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added

   solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1
    
   #print(solution.route_vertices[i, vehicle_type_index, vehicle_id])
    
   #saber de onde vem os dados
   #instance = GetInstanceData()
    
   #if  instance.multi_trip == True:
      #EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id)
   #else:
      #EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id)

   return solution

def AddVertex3(solution, vertex_to_be_added, vehicle_type_index, vehicle_id, position, penalty):


    
   #solution.vertices_visited[vertex_to_be_added] += 1
   #print(position)

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
   for i in range(rota_do_vertice_cnt, position, -1):
      print(i)
      #.route_vertices(vehicle_type_index, vehicle_id, i + 1) = .route_vertices(vehicle_type_index, vehicle_id, i) -> perguntar
      #solution.route_vertices[i, vehicle_type_index, vehicle_id] = solution.route_vertices[i-1, vehicle_type_index, vehicle_id]
            

        
   #dimensão, linha e coluna
   #solution.route_vertices[position, vehicle_type_index, vehicle_id] = vertex_to_be_added

   solution.route_vertex_cnt[vehicle_type_index, vehicle_id] += 1
    
   #print(solution.route_vertices[i, vehicle_type_index, vehicle_id])
    
   #saber de onde vem os dados
   #instance = GetInstanceData()
    
   #if  instance.multi_trip == True:
      #EvaluateRouteMultiTrip2(solution, vehicle_type_index, vehicle_id)
   #else:
      #EvaluateRouteSingleTrip2(solution, vehicle_type_index, vehicle_id)

   return solution




def ImproveSolution2(solution, penalty):

   #para saber de qual é a classe
   #print(solution.route_vertices)
   #solution = Solution_Data()
   #é Long -> é inteiro estendido
   #é Integer -> é inteiro
   iI = 0 # é Long
   jI = 0 # é Long
   kI = 0 #é Long
    
   aI = 0 # é Long
   bI = 0 # é Long
   cI = 0 # é Long
    
   #vertex = [] # é Long
   vertex = 0
   #vertex_buffer = [] # é  Long
   vertex_buffer = np.zeros((vertex_list.num_customers), dtype ='int16')
   # é Long
   for improvement_iterations in range(0, max_improvement_iterations+1):
                    
      #relocate -> realocar
      vehicle_type_to_relocate1 = -1
      #For i = 1 To vehicle_type_list.num_vehicle_types
      for i  in range(0, vehicle_type_list.num_vehicle_types):
         #For j = 1 To vehicle_type_list.vehicle_types[i].NumberAvailable
         for j  in range(0, vehicle_type_list.vehicle_types[i].NumberAvailable):
            for k  in range(0, solution.route_vertex_cnt[i, j]):
               #vertex = solution.route_vertices[k, i, j]
                         
               RemoveVertex2(solution, i, j, k, penalty)


               #For a = 1 To vehicle_type_list.num_vehicle_types
               #for a  in range(0, vehicle_type_list.num_vehicle_types):
                  #For b = 1 To vehicle_type_list.vehicle_types[a].NumberAvailable
                  #for b in range(0, vehicle_type_list.vehicle_types[a].NumberAvailable):
                  #For c = 1 To .route_vertex_cnt[a, b] + 1
                     #for c  in range(0, solution.route_vertex_cnt[a, b] +1):

                        #AddVertex2(solution, vertex, a, b, c, penalty)

                                
                                    

                        #RemoveVertex2(solution, a, b, c, penalty)

                        #print(c)
               
               #AddVertex3(solution, vertex, i, j, k, penalty)
               
      #if ( ((vehicle_type_to_swap1 != -1) or  (vehicle_type_to_relocate1 != -1) or (vehicle_type_for_2opt1 != -1) or (vehicle_type_for_chain_reversal != -1) or (vehicle_type_for_full_swap1 != -1)) and improvement_iterations > max_improvement_iterations):
         #break

   return solution