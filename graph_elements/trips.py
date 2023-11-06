class Trips():
    
    def __init__(self, trip_id, route_id, service_id, trip_headsign):
        self.trip_id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.trip_headsign = trip_headsign
        
    def add_direction(self, direction):
        self.direction_id = direction
        self.opposite_direction = not bool(direction)
        
    def to_dictionary(self) -> dict:
        data = {
            "trip-id" : int(self.trip_id),
            "route-id" : int(self.route_id),
            "service-id" : self.service_id,
            "direction-id" : int(self.direction_id),
            "opposite-direction" : self.opposite_direction,
            "trip-headsign" : self.trip_headsign
        }
        
        return data