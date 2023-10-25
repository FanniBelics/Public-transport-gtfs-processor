import math as math

EARTH_RADIUS_KM = 6371

class Node():

    def __init__(self, id, name, short_name, desc, lon, lat):
        self.gtfs_id = id
        self.name = name
        self.short_name = short_name
        self.description = desc
        self.longitude = lon
        self.latitude = lat
        self.parental_node 
        self.children = set()

    def __str__(self) -> str:
        return "{0}, {1}, {2}, {3}".format(self.gtfs_id, self.name, self.latitude, self.longitude)

    def __eq__(self, otherNode: "Node") -> bool:
        return self.longitude == otherNode.longitude and self.latitude == otherNode.latitude
    
    def __ne__(self, otherNode: "Node") -> bool:
       return self.longitude != otherNode.longitude or self.latitude != otherNode.latitude
    
    def __sizeof__(self) -> int:
        return self.parental_node.size()
    
    def __hash__(self) -> int:
        return hash(self.gtfs_id)
    
    def calculate_dist(self, otherNode: "Node") -> float:
        return math.acos(math.sin(self.latitude) * math.sin(otherNode.latitude) + math.cos(self.latitude)*math.cos(otherNode.latitude) 
                         *math.cos(otherNode.longitude - self.longitude)) * EARTH_RADIUS_KM
    
    def set_parental_node(self,parent_node_id: int):
        self.parental_node = parent_node_id
        
    def add_child_node(self, mother_node: "Node"):
        mother_node.children.add(self.gtfs_id)
    


# acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371