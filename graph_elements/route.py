class Route():
    
    def __init__(self, route_id, agency_id, route_short, route_desc):
        self.route_id = route_id
        self.agency_id = agency_id
        self.route_short_name = route_short
        self.route_description = route_desc
        self.stops = []
        self.trips = []
        
    def add_long_name(self, long_name: str):
        if(long_name == ''):
            self.route_long_name = self.route_short_name
        else:
            self.route_long_name = long_name
            
    def add_route_type(self, route_type: str):
        self.route_type = route_type
        match route_type:
            case '0':
                self.route_type_str = "Tram, Streetcar, Light rail"
            case '1':
                 self.route_type_str = "Subway, Metro"
            case '2':
                self.route_type_str = "Rail"
            case '3':
                self.route_type_str = "Bus"
            case '4':
                self.route_type_str = "Ferry"
            case '5':
                self.route_type_str = "Cable tram"
            case '6':
                self.route_type_str = "Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway)"
            case '7':
                self.route_type_str = "Funicular"
            case '11':
                self.route_type_str = "Trolleybus"
            case '12':
                self.route_type_str = "Monorail"
            case _:
                self.route_type_str = 'Unknown'
                
    def add_stop(self, stop_id: int):
        self.stops.append(stop_id)
        
    def add_trip(self, trip_id: int):
        self.trips.append(trip_id)
        
    def to_dictionary(self) -> dict:
        data = {
            "route-id" : int(self.route_id),
            "agency-id" : self.agency_id,
            "route-type" : int(self.route_type),
            "route-type-as-text" : self.route_type_str,
            "route-short-name" : self.route_short_name,
            "route-long-name" : self.route_long_name,
            "route-description" : self.route_description
        }
        
        if len(self.stops) > 0:
            data.update({"stops" : self.stops})
        
        if len(self.trips) > 0:
            data.update({"trips" : self.trips})
        
        return data