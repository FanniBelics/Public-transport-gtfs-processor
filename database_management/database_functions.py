from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os,sys, path

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip, stop_to_dictionary
from graph_elements.edge import Edge

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
ROUTES_COLLECTION = os.environ.get("COLLECTION_ROUTES_NAME")
TRIPS_COLLECTION = os.environ.get("COLLECTION_TRIPS_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()


connection_string=f"mongodb+srv://belics_fanni:{PASSWORD}@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

database = client[DICTIONARY]

def to_route(candidate: dict) -> Route:
    route = Route(candidate["route-id"], 
                  candidate["agency-id"], candidate["route-short-name"], 
                  candidate["route-description"])
    route.route_long_name = candidate["route-long-name"]
    route.route_type = candidate["route-type"]
    route.route_type_str = candidate["route-type-as-text"]
    
    if "stops-reached" in candidate.keys():
        route.stops = candidate["stops-reached"]
        
    if "trips" in candidate.keys():
        route.trips = candidate["trips"]
    
    return route
        
def to_node(candidate: dict) -> Node:
    node = Node(candidate["gtfs-id"], candidate["name"], 
                candidate["short-name"],candidate["description"], 
                candidate["longitude"], candidate["latitude"])
    if "parental-node" in candidate.keys():
        node.parental_node = candidate["parental-node"]
    else:
        node.parental_node = None
            
    if "children" in candidate.keys():
        node.children = candidate["children"]
    else:
        node.children = []
            
    if "routes" in candidate.keys():
        node.routes = candidate["routes"]
            
    return node

def to_trip(candidate: dict) -> Trip:
    trip = Trip(candidate["trip-id"], candidate["route-id"],
                candidate["service-id"], candidate["trip-headsign"])
    trip.add_direction(candidate["direction-id"])
    
    return trip

def upload_node_to_database(node: Node) -> bool:
    data = node.to_dictionary()
    try:
        database[NODES_COLLECTION].insert_one(data)
        
    except Exception as e:
        print(e)
        return False
    
    else:
        return True
    
def upload_route_to_database(route: Route):
    data = route.to_dictionary()
    try:
        database[ROUTES_COLLECTION].insert_one(data)
        
    except Exception as e:
        print(e)
        return False
    
    else:
        return True
    
def upload_trip_to_database(trip: Trip):
    data = trip.to_dictionary()
    try:
        database[TRIPS_COLLECTION].insert_one(data)
    
    except Exception as e:
        print(e)
        return False
    
    else:
        return True
    
def upload_edge_to_database(edge: Edge):
    data = edge.to_dictionary()
    try:
        database[EDGES_COLLECTION].insert_one(data)
    
    except Exception as e:
        print(e)
        return False
    
    else:
        return True

def add_parental_node_to_node(node: Node, parent: int):
    try:
        database[NODES_COLLECTION].update_one({"gtfs-id" : int(node.gtfs_id)},
                                              {"$set": {"parental-node" : int(parent)}})
    except Exception as e:
        print(e)
    
def add_child_to_node(node: int, child: int): 
    try:
        database[NODES_COLLECTION].update_one({"gtfs-id" : int(node)},
                                              {"$push" : {"children" : int(child)}})
    except Exception as e:
        print(e)
        
def add_stop_to_route(route: int, stop: int):
    try:
        database[ROUTES_COLLECTION].update_one({"route-id" : int(route)},
                                                {"$push" : {"stops-reached" : int(stop)}})
    except Exception as e:
        print(e)
        
def add_trip_to_route(route: int, trip: int):
    try:
        database[ROUTES_COLLECTION].update_one({"route-id" : int(route)},
                                                {"$push" : {"trips" : int(trip)}})
    except Exception as e:
        print(e)

def add_stop_to_trip(trip: int, stop: list):
    try:
        database[TRIPS_COLLECTION].update_one({"trip-id" : int(trip)},
                                                {"$push" : {"stops-reached" : stop_to_dictionary(stop)}})
    except Exception as e:
        print(e)

def find_node_by_gtfs_id(gtfs_id: int) -> Node: 
    return to_node(database[NODES_COLLECTION].find_one({'gtfs-id': int(gtfs_id)}))

def find_route_by_id(route_id: int) -> Route:
    return to_route(database[ROUTES_COLLECTION].find_one({"route-id" : int(route_id)}))

def find_trip_by_id(trip_id: int) -> Trip:
    return to_trip(database[TRIPS_COLLECTION].find_one({"trip-id" : int(trip_id)}))

def add_stops_to_trip(trip: Trip):
    database[TRIPS_COLLECTION].update_one({"trip-id" : trip.trip_id},
                                          {"$set" : {trip.stops_to_dictionary()}}) 
    
