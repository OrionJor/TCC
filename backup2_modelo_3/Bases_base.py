
#Abrir e fechar arquivos
#from os import close


epsilon = 0.0001
max_improvement_iterations = 50
offset_constant = 17


class Vertex_Data(object):

    def __init__ (self, service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end):
        self.service_time = service_time
        self.mandatory = mandatory
        self.profit = profit
        self.pickup_amount = pickup_amount
        self.delivery_amount = delivery_amount
        self.time_windows_start = time_windows_start
        self.time_windows_end = time_windows_end


    def __repr__(self):
        return str(self.__dict__)


class Vertex_List_Data(Vertex_Data):
    def __init__(self):
        self.num_depots = None
        self.num_customers = None
        self.num_locations = None
        self.vertices = []

    def set_Vertex_list(self):
        return self.num_depots, self.num_customers, self.num_locations
        

    def get_Vertex_list(self):
        return self.num_depots, self.num_customers, self.num_locations

    
    def get_Vertex_Data(self, service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end):
        cave = Vertex_Data(service_time, mandatory, profit, pickup_amount, delivery_amount, time_windows_start, time_windows_end)
        self.vertices.append(cave)
        
        return self.vertices
    
    def __iter__(self):
        for value in self.vertices:
            return value


class Vehicle_Type_Data:
    def __init__(self, capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, 
    number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id):

        self.capacity = capacity
        self.fixed_cost_per_trip = fixed_cost_per_trip
        self.cost_per_unit_distance = cost_per_unit_distance
        self.duration_multiplier = duration_multiplier
        self.number_available = number_available
        self.work_start_time = work_start_time
        self.distance_limit = distance_limit
        self.driving_time_limit = driving_time_limit
        self.working_time_limit = working_time_limit
        self.origin_base_id = origin_base_id
        self.return_base_id = return_base_id
        self.type = type_id

    def __repr__(self):
        return str(self.__dict__)


class Vehicle_Type_List_Data(Vehicle_Type_Data):
    def __init__(self):
        self.num_vehicle_types = None
        self.vehicle_types = []
        self.compatible = []
    
    def set_vehicle_type_list_data(self):
        return self.num_vehicle_types
    
    def get_vehicle_type_list_data(self):
        return self.num_vehicle_types

    def create_Vehicle_Type_List_Data(self, capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id):
        cave = Vehicle_Type_Data(capacity, fixed_cost_per_trip, cost_per_unit_distance, duration_multiplier, number_available, work_start_time, distance_limit, driving_time_limit, working_time_limit, origin_base_id, return_base_id, type_id)
        self.vehicle_types.append(cave)
        

    def __iter__(self):
        for value in self.vehicle_types:
            return value


class Arc_Data:
    def __init__(self):
        self.distance = []
        self.duration = []


class Instance_Data:

    def __init__(self):
        self.open_vrp = None
        self.multi_trip = None
        self.penalty = None
        self.soft_time_windows = None
        self.backhauls = None
        self.vehicle_location_incompatibility = None
        self.num_depots = None
        self.num_customers = None
        self.num_locations = None 
        self.num_vehicle_types = None

    def set_instance_data(self):
        return self.open_vrp, self.multi_trip, self.penalty, self.soft_time_windows, self.backhauls, self.vehicle_location_incompatibility, self.num_depots, self.num_customers, self.num_locations, self.num_vehicle_types


    def get_instance_data(self):
        return self.open_vrp, self.multi_trip, self.penalty, self.soft_time_windows, self.backhauls, self.vehicle_location_incompatibility, self.num_depots, self.num_customers, self.num_locations, self.num_vehicle_types



class Solution_Data:
    def __init__(self):
        self.feasible = None
        self.covers_mandatory_vertices = None
        self.net_profit = None
        self.total_distance = None
        self.net_profit_per_route = []
        self.total_distance_per_route = []
        self.route_vertex_cnt = []
        self.route_vertices = []
        self.vertices_visited = []
    
    def set_solution_data(self):
        return self.feasible, self.covers_mandatory_vertices, self.net_profit, self.total_distance

    def get_solution_data(self):
        return self.feasible, self.covers_mandatory_vertices, self.net_profit, self.total_distance


class Solver_Option_Data:
    def __init__(self):
        self.CPU_time_limit = None
        self.LNS_minimum_removal_rate = None
        self.LNS_maximum_removal_rate = None
        self.LNS_candidate_list_size = None
        self.warm_start  = None
        self.status_updates = None

    def set_solver_option_data(self):
        return self.CPU_time_limit, self.LNS_minimum_removal_rate, self.LNS_maximum_removal_rate,  self.LNS_candidate_list_size, self.warm_start, self.status_updates

    def get_set_solver_option_data(self):
        return self.CPU_time_limit, self.LNS_minimum_removal_rate, self.LNS_maximum_removal_rate,  self.LNS_candidate_list_size, self.warm_start, self.status_updates



class Candidate_Data:
    def __init__(self):
        self.mandatory = None
        self.net_profit = None
        self.total_distance = None
        self.vertex_to_be_added = None
        self.vehicle_type_index = None
        self.vehicle_id = None
        self.position = None

    def set_candidate_data(self):
        return self.mandatory, self.net_profit, self.total_distance, self.vertex_to_be_added, self.vehicle_type_index, self.vehicle_id, self.position

    def get_candidate_data(self):
        return self.mandatory, self.net_profit, self.total_distance, self.vertex_to_be_added, self.vehicle_type_index, self.vehicle_id, self.position


class DP_Data:
    def __init__(self):
        value = []
        control = []