from .node import *

class Edge():
    
    def __init__(self, id, fromStop: Node, toStop: Node) -> None:
        self.id = id
        self.fromStop = fromStop
        self.toStop = toStop
        self.distance = 0
        self.travelling_time_mins = 0
        self.travelling_time_secs = 0
        
    def __str__(self) -> str:
        return "From {0} to {1}".format(self.fromNode, self.toNode)
    
    def __eq__(self, otherEdge: "Edge") -> bool:
        return self.fromNode == otherEdge.fromNode and self.toNode == otherEdge.toNode
    
    def __ne__(self, otherEdge: "Edge") -> bool:
        return self.fromNode != otherEdge.fromNode and self.toNode != otherEdge.toNode
    
    def __lt__(self, otherEdge: "Edge") -> bool:
        return self.distance < otherEdge.distance
    
    def __le__(self, otherEdge: "Edge") -> bool:
        return self.distance <= otherEdge.distance
    
    def __gt__(self, otherEdge: "Edge") -> bool:
        return self.distance > otherEdge.distance
    
    def __ge__(self, otherEdge: "Edge") -> bool:
        return self.distance >= otherEdge.distance
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def set_distance(self, currentTravelled: float, perviousTravelled: float):
        self.distance = abs(currentTravelled - perviousTravelled)
        
    def set_from_stop(self, fromStop):
        self.fromStop = fromStop
        
    def set_travelling_time(self, current: str, previous: str):
        current_split = [int(n) for n in current.split(':')]
        previous_split = [int(n) for n in previous.split(':')]

        if previous_split[2] > current_split[2]:
            self.travelling_time_secs = (current_split[2] + 60) - previous_split[2]
            current_split[1] -= 1
        else:
            self.travelling_time_secs = current_split[2] - previous_split[2]

        if previous_split[1] > current_split[1]:
            self.travelling_time_mins = (current_split[1] + 60) - previous_split[1]
            current_split[0] -= 1 
        else:
            self.travelling_time_mins = current_split[1] - previous_split[1]

        self.travelling_time_hours = current_split[0] - previous_split[0]

        self.travelling_time_mins += self.travelling_time_hours * 60

        
    def set_departure_time(self, departure: str):
        self.departure_h, self.departure_m, self.departure_s = departure.split(":")
        
    def get_departure_time(self) -> str:
        return ":".join([self.departure_h, self.departure_m, self.departure_s])
        
    def set_arrival_time(self, arrival: str):
        self.arrival_h, self.arrival_m, self.arrival_s = arrival.split(":")
        
    def set_owner_trip(self, trip_id: int):
        self.owner_trip = int(trip_id)
    
    def set_owner_route(self, route_id: int):
        self.owner_route = int(route_id)
        
    def to_dictionary(self) -> dict:
        data = {
            "id" : self.id,
            "from-stop" : int(self.fromStop),
            "to-stop" : int(self.toStop),
            "distance" : float(self.distance),
            "travelling-time-mins" : int(self.travelling_time_mins),
            "travelling-time-secs" : int(self.travelling_time_secs),
            "departure-time" : {
                "hour" : int(self.departure_h),
                "minute" : int(self.departure_m),
                "second" : int(self.departure_s)
            },
            "owner-trip" : int(self.owner_trip),
            "owner-route" : int(self.owner_route)
        }
        
        return data