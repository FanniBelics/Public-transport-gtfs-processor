import math as math

EARTH_RADIUS_KM = 6371

class Node():
    
    parental_node = set()

    def __init__(self, id, name, lon, lat):
        self.id = id
        self.name = name
        self.longitude = lon
        self.latitude = lat

    def __str__(self) -> str:
        return "{0}, {1}".format(self.id, self.name)

    def __eq__(self, otherNode: "Node") -> bool:
        return self.longitude == otherNode.longitude and self.latitude == otherNode.latitude
    
    def __ne__(self, otherNode: "Node") -> bool:
       return self.longitude != otherNode.longitude or self.latitude != otherNode.latitude
    
    def __sizeof__(self) -> int:
        return self.parental_node.size()
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def calculate_dist(self, otherNode: "Node") -> float:
        return math.acos(math.sin(self.latitude) * math.sin(otherNode.latitude) + math.cos(self.latitude)*math.cos(otherNode.latitude) 
                         *math.cos(otherNode.longitude - self.longitude)) * EARTH_RADIUS_KM
    
    def setParentalNode(self,parentNode: "Node"):
        self.parental_node.add(parentNode)
        


# acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371