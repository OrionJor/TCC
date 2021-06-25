

class Vertex_Data(object):

    def __init__ (self, service_time, time_windows_start):
        self.service_time = service_time
        self.time_windows_start =time_windows_start


    def __repr__(self):
        return str(self.__dict__)


class Vertex_List_Data(Vertex_Data):
    def __init__(self):
        self.num_depots = None
        self.num_customers = None
        self.num_locations = None
        self.vertices = []

    def set_Vertex_list(self, num_customers, num_locations, num_despots, vertices):
        self.num_depots = num_despots
        self.num_customers = num_customers
        self.num_locations = num_locations
        self.vertices = vertices
        
    
    def get_Vertex_list(self):
        return self.num_depots, self.num_customers, self.num_locations, self.vertices