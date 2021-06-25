

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

    def set_Vertex_list(self, num_customers, num_locations, num_despots):
        self.num_depots = num_despots
        self.num_customers = num_customers
        self.num_locations = num_locations
        
    
    def get_Vertex_list(self):
        return self.num_depots, self.num_customers, self.num_locations

    def Time_Converter(tempo, interval = "secs"):

        hora = tempo.hour
        minutos = tempo.minute
        segundos = tempo.second
        
        '''
        def yrs():
        return divmod(duration_in_s, yr_ct)[0]

        def days():
        return divmod(duration_in_s, day_ct)[0]
        
        def hrs():
        return divmod(duration_in_s, hour_ct)[0]

        '''
        def mins():
            resutado  = (hora*60) + minutos + (segundos /60)
            return resutado
        '''
        def secs(): 
        return duration_in_s
        '''
        return {
            'mins': int(mins())
            #'secs': int(secs())
        }[interval]

    
    def get_Vertex_Data(self,  service_time, time_windows_start):
        cave = Vertex_Data(service_time, time_windows_start)
        self.vertices.append(cave)
        
        return self.vertices
    
    def __iter__(self):
        for value in self.vertices:
            return value