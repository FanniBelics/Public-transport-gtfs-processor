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

    def __eq__(self, othetNode: Node) -> bool:
        return self.id == othetNode.id
    
    def __ne__(self, otherNode: Node) -> bool:
        return self.id != otherNode.id
    
    def calculate_dist(self, otherNode: Node) -> float:
        return math.acos(math.sin(self.latitude) * math.sin(otherNode.latitude) + math.cos(self.latitude)*math.cos(otherNode.latitude) 
                         *math.cos(otherNode.longitude - self.longitude)) * EARTH_RADIUS_KM
    
    def setParentalNode(self,parentNode: Node):
        self.parental_node.add(parentNode)


# acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371