from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os


from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip, stop_to_dictionary
from graph_elements.edge import Edge
from graph_elements.solution_holder import Solution_Holder

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
ROUTES_COLLECTION = os.environ.get("COLLECTION_ROUTES_NAME")
TRIPS_COLLECTION = os.environ.get("COLLECTION_TRIPS_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()
SOLUTIONS_COLLECTION = os.environ.get("COLLECTION_SOLUTIONS_NAME")


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
                candidate["service-id"], candidate["trip_headsign"])
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
    

#---- Functions for processing ----
def get_all_stops():
    stops = database[NODES_COLLECTION].find({},{})
    converted_stops = []
    for stop in stops:
         converted_stops.append(to_node(stop))
        
    return converted_stops

def is_stop_on_same_route(stop1: Node, stop2: Node) -> bool:
   data = list(database[ROUTES_COLLECTION].find({"stops-reached" : {"$all" : [stop1.gtfs_id, stop2.gtfs_id]}}))
   return len(data) > 0

def find_routes_by_stop_id(stop_id: int) -> "list[int]":
    return list(database[ROUTES_COLLECTION].find({"stops-reached" : stop_id},
                                                 {"route-id":1, "route-short-name":1, "stops-reached":1, "_id":0}))
    
def find_routes_by_stop_id_and_exception_routes(stop_id: int, route_id_list: list = []) -> "list[int]":
    return list(database[ROUTES_COLLECTION].find({"$and" :[{"stops-reached" : stop_id,
                                                           "route-id" : {"$nin" : route_id_list}}]},
                                                 {"route-id":1, "route-short-name":1, "stops-reached":1, "_id":0}))
    
def get_all_routes() -> "list[Route]":
    data =  list(database[ROUTES_COLLECTION].find({}))
    data = [to_route(route) for route in data]
    return data

def solution_exists_in_db(fromStop: int, toStop: int):
    return database[SOLUTIONS_COLLECTION].count_documents({"from-id": fromStop, "to-id": toStop}) > 0

def upload_solution(solution: dict):
    database[SOLUTIONS_COLLECTION].insert_one(solution)
    
def add_path_to_solution(fromStop: int, toStop:int, pathway: list[dict]):
    database[SOLUTIONS_COLLECTION].update_one({"from-id": fromStop, "to-id": toStop}, 
                                              {"$push": {"changes": pathway}})
    
def clear_sol():
    database[SOLUTIONS_COLLECTION].delete_many({})
    
def find_solution_by_from_stop(fromStop: int) -> "list[Solution_Holder]":
    return Solution_Holder(database[SOLUTIONS_COLLECTION].find({"from-id": fromStop}))

def find_solution_by_from_stop_and_to_stop(fromStop: int, toStop: int) -> "list[Solution_Holder]":
    return Solution_Holder(database[SOLUTIONS_COLLECTION].find({"from-id": fromStop,
                                                                              "to-id": toStop}))

def get_all_solutions():
    data = database[SOLUTIONS_COLLECTION].find({})
    li = []
    for element in data:
        sol = Solution_Holder(element["from-id"], element["to-id"])
        sol.addChangeDict(element["changes"])
        li.append(sol)
        
    return li

def is_there_alternative(fromStop: int, toStop: int, route: int):
    if database[SOLUTIONS_COLLECTION].find(
        {
            "changes" : {
                "$elemMatch": {
                     "$elemMatch": {
                        "from-stop-partial": fromStop,
                        "to-stop-partial":toStop,
                        "route-id" : route
                        }
                    }
            }}):
            return True
    #TODO
    
    
def get_stopSets_by_fromStop(fromStop: int, route: list) -> list:
    data =  database[SOLUTIONS_COLLECTION].find({
        "from-id": fromStop,
        "changes" : {
        "$not" : {
            "$elemMatch" : {
                "route-id" : route
            }
        }
    }},
    {
        "changes" : 1,
         "_id" : 0
    })
    
    data = [changes["changes"] for changes in data]
    candidates = []
    for pair in data:
        for change_set in pair:
            if all(change_pair["route-id"] not in route for change_pair in change_set):
                candidates.append(change_set)
    return candidates


def get_edge_transferTimes(fromStop: int, toStop: int):
    return list(database[EDGES_COLLECTION].find({
        "from-stop": fromStop,
        "to-stop" : toStop
    },{
        "_id": 0, "travelling-time-mins" : 1, "travelling-time-secs" : 1
    }))