from .node import *

class Edge():
    
    def __init__(self, id, fromNode: Node, toNode: Node) -> None:
        self.id = id
        self.fromNode = fromNode
        self.toNode = toNode
        self.distance = 0
        
    def __str__(self) -> str:
        return "From {0} to {1}".format(self.fromNode, self.toNode)
    
    def set_distance(self) -> None:
        self.set_distance = self.fromNode.calculate_dist(self.toNode)
        
    def get_distance(self) -> float:
        return self.distance
    
    def __eq__(self, otherEdge: Edge) -> bool:
        return self.fromNode == otherEdge.fromNode and self.toNode == otherEdge.toNode
    
    def __ne__(self, otherEdge: Edge) -> bool:
        return self.fromNode != otherEdge.fromNode and self.toNode != otherEdge.toNode
    
    def __lt__(self, otherEdge: Edge) -> bool:
        return self.distance < otherEdge.distance
    
    def __le__(self, otherEdge: Edge) -> bool:
        return self.distance <= otherEdge.distance
    
    def __gt__(self, otherEdge: Edge) -> bool:
        return self.distance > otherEdge.distance
    
    def __ge__(self, otherEdge: Edge) -> bool:
        return self.distance >= otherEdge.distance