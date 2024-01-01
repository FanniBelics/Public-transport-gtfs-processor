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
            "stop-type-str" : self.stop_type_str
        }
        
        elements_dict = self.stops_to_dictionary()
        data.update(elements_dict)
        
        return data
    
    def stops_to_dictionary(self: "Trip") -> dict:
        elements = []
        if len(self.stops_reached) > 0:
            for stop in self.stops_reached:
                stop_dict = {
                    "stop-id" : int(stop[0]),
                    "stop-time" : {
                        "hour" : int(stop[1][0]),
                        "minute" : int(stop[1][1]),
                        "second" : int(stop[1][2]),
                    }
                }
                elements.append(stop_dict)
        
        return {"stops-reached" : elements}
    
def stop_to_dictionary(stop) -> dict:
    stop_dict = {
                "stop-id" : int(stop[0]),
                "stop-time" : {
                    "hour" : int(stop[1][0]),
                    "minute" : int(stop[1][1]),
                    "second" : int(stop[1][2]),
                }
    }
    return stop_dict