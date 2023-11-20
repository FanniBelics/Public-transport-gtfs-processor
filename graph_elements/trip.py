class Trip():
    
    def __init__(self, trip_id, route_id, service_id, trip_headsign):
        self.trip_id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.trip_headsign = trip_headsign
        self.stops_reached = []
        
    def add_direction(self, direction):
        self.direction_id = direction
        self.opposite_direction = direction == '1'
        
    def add_reached_stop(self, stop_id: str, stop_time: str):
        self.stops_reached.append((stop_id, stop_time.split(":")))
        
    def add_stop_type(self, stop_type):
        self.stop_type = stop_type
        match(stop_type):
            case '0':
                self.stop_type_str = "First stop"
            case '1':
                self.stop_type_str = "None"
            case '2':
                self.stop_type_str = "Last stop"
        
    def to_dictionary(self) -> dict:
        data = {
            "trip-id" : int(self.trip_id),
            "route-id" : int(self.route_id),
            "service-id" : self.service_id,
            "direction-id" : int(self.direction_id),
            "opposite-direction" : self.opposite_direction,
            "trip-headsign" : self.trip_headsign,
            "stop-type" : int(self.stop_type),
            "stop-type-str" : self.stop_type_str,
        }
        
        
        
        return data