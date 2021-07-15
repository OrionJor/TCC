
#Abrir e fechar arquivos
#from os import close


epsilon = 0.0001
max_improvement_iterations = 50
offset_constant = 17


class Vertex_Data(object):

    def __init__ (self, service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end):
        self.ServiceTime = service_time
        self.mandatory = mandatory
        self.profit = profit
        self.PickupAmount = pickup_amount
        self.DeliveryAmount = delivery_amount
        self.TimeWindowsStart = time_windows_start
        self.TimeWindowsEnd = time_windows_end

    def __repr__(self):
        return str(self.__dict__)


class Vertex_List_Data(Vertex_Data):
    def __init__(self):
        self.num_depots = 0
        self.num_customers = 0
        self.num_locations = 0
        self.vertices = []

    def set_Vertex_list(self, num_depots, num_customers, num_locations):
        self.num_depots = num_depots
        self.num_customers = num_customers
        self.num_locations = num_locations
        

    def get_Vertex_list(self):
        return self.num_depots, self.num_customers, self.num_locations

    
    def get_Vertex_Data(self, service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end):
        cave = Vertex_Data(service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end)
        self.vertices.append(cave)
        
        return self.vertices
    
    def __iter__(self):
        for value in self.vertices:
            return value

#vertex_list = Vertex_List_Data()

class Vehicle_Type_Data:
    def __init__(self, capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, 
    number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id):

        self.capacity = capacity
        self.FixedCostPerTrip = fixed_cost_per_trip
        self.CostPerUnitDistance = cost_per_unit_distance
        self.DurationMultiplier = duration_multiplier
        self.NumberAvailable = number_available
        self.WorkStartTime = work_start_time
        self.DistanceLimit = distance_limit
        self.DrivingTimeLimit = driving_time_limit
        self.WorkingTimeLimit = working_time_limit
        self.OriginBaseId = origin_base_id
        self.ReturnBaseId = return_base_id
        self.type = type_id

    def __repr__(self):
        return str(self.__dict__)


class Vehicle_Type_List_Data(Vehicle_Type_Data):
    def __init__(self):
        self.num_vehicle_types = 0
        self.vehicle_types = []
        self.compatible = []
    
    def set_vehicle_type_list_data(self, num_vehicle_types):
        self.num_vehicle_types = num_vehicle_types
    
    def get_vehicle_type_list_data(self):
        return self.num_vehicle_types

    def create_Vehicle_Type_List_Data(self, capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id):
        cave = Vehicle_Type_Data(capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id)
        self.vehicle_types.append(cave)
        

    def __iter__(self):
        for value in self.vehicle_types:
            return value

#vehicle_type_list = Vehicle_Type_List_Data()

class Arc_Data:
    def __init__(self):
        self.distance = []
        self.duration = []

#arc_list = Arc_Data()

class Instance_Data:

    def __init__(self):
        self.open_vrp = None
        self.multi_trip = None
        self.penalty = 0
        self.soft_time_windows = None
        self.backhauls = None
        self.vehicle_location_incompatibility = None
        self.num_depots = 0
        self.num_customers = 0
        self.num_locations = 0 
        self.num_vehicle_types = 0

    def set_instance_data(self, open_vrp, multi_trip, penalty, soft_time_windows, backhauls, vehicle_location_incompatibility, num_depots, num_customers, num_locations, num_vehicle_types):
        self.open_vrp = open_vrp
        self.multi_trip = multi_trip
        self.penalty = penalty
        self.soft_time_windows = soft_time_windows
        self.backhauls = backhauls
        self.vehicle_location_incompatibility = vehicle_location_incompatibility
        self.num_depots = num_depots
        self.num_customers = num_customers
        self.num_locations = num_locations
        self.num_vehicle_types = num_vehicle_types


    def get_instance_data(self):
        return self.open_vrp, self.multi_trip, self.penalty, self.soft_time_windows, self.backhauls, self.vehicle_location_incompatibility, self.num_depots, self.num_customers, self.num_locations, self.num_vehicle_types

#instance = Instance_Data()

class Solution_Data:
    def __init__(self):
        self.feasible = None
        self.covers_mandatory_vertices = None
        self.net_profit = 0
        self.total_distance = 0
        self.net_profit_per_route = []
        self.total_distance_per_route = []
        self.route_vertex_cnt = []
        self.route_vertices = []
        self.vertices_visited = []
    
    def set_solution_data(self, feasible, covers_mandatory_vertices, net_profit, total_distance):
        self.feasible = feasible
        self.covers_mandatory_vertices =  covers_mandatory_vertices
        self.net_profit = net_profit
        self.total_distance = total_distance

    def get_solution_data(self):
        return self.feasible, self.covers_mandatory_vertices, self.net_profit, self.total_distance



class Solver_Option_Data:
    def __init__(self):
        self.CPU_time_limit = 0
        self.LNS_minimum_removal_rate = 0
        self.LNS_maximum_removal_rate = 0
        self.LNS_candidate_list_size = 0
        self.warm_start  = None
        self.status_updates = None

    def set_solver_option_data(self, CPU_time_limit, LNS_minimum_removal_rate, LNS_maximum_removal_rate,  LNS_candidate_list_size, warm_start, status_updates):
        self.CPU_time_limit = CPU_time_limit
        self.LNS_minimum_removal_rate = LNS_minimum_removal_rate
        self.LNS_maximum_removal_rate = LNS_maximum_removal_rate
        self.LNS_candidate_list_size = LNS_candidate_list_size
        self.warm_start = warm_start
        self.status_updates = status_updates

    def get_set_solver_option_data(self):
        return self.CPU_time_limit, self.LNS_minimum_removal_rate, self.LNS_maximum_removal_rate,  self.LNS_candidate_list_size, self.warm_start, self.status_updates

#solver_options = Solver_Option_Data()

class Candidate_Data:
    def __init__(self, mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position):
        self.mandatory = mandatory
        self.NetProfit = net_profit
        self.TotalDistance = total_distance
        self.VertexToBeAdded = vertex_to_be_added
        self.VehicleTypeIndex = vehicle_type_index
        self.VehicleId = vehicle_id
        self.position = position

    def set_candidate_data(self, mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position):
        self.mandatory =  mandatory
        self.NetProfit = net_profit
        self.TotalDistance = total_distance
        self.VertexToBeAdded = vertex_to_be_added
        self.VehicleTypeIndex = vehicle_type_index
        self.VehicleId = vehicle_id
        self.position = position

    def get_candidate_data(self):
        return self.mandatory, self.NetProfit, self.TotalDistance, self.VertexToBeAdded, self.VehicleTypeIndex, self.VehicleId, self.position

    def __repr__(self):
        return str(self.__dict__)

class Candidate(Candidate_Data):
    def __init__(self):
        self.candidate_list = []

    def create_candidate(self, mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position):
        cave = Candidate_Data(mandatory, net_profit, total_distance, vertex_to_be_added, vehicle_type_index, vehicle_id, position)
        self.candidate_list.append(cave)


class DP_Data:
    def __init__(self):
        self.value = []
        self.control = []

#DP_list = DP_Data()