from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip
from graph_elements.edge import Edge
from graph_elements.solution_holder import Solution_Holder
import database_management.database_functions as database_functions
import asyncio
from statistics import mean
import math


MAX_CHANGES = 10
WALK_SPEED = 5

def is_close(first_stop: Node, second_stop: Node):
    if first_stop == second_stop:
        return True
    
     #The average walking speed understood in km/h
    distance = first_stop.calculate_dist(second_stop)
    return round((distance / WALK_SPEED)*60) <= 5 #the time it takes to walk the distance

def haversine(coord_a, coord_b):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1 = coord_a
    lat2, lon2 = coord_b
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.asin(math.sqrt(a)))  # Distance in km

def calculate_walking_time(coord_a, coord_b):
    distance_km = haversine(coord_a, coord_b)
    return distance_km / 5 * 60  # Walking speed ~5 km/h, return time in minutes

def calculate_complete_time(from_time: dict, to_time: dict) -> int:
    return (to_time["hour"] - from_time["hour"])*60 + to_time["minute"] - from_time["minute"]

def isTimingCorrect(candidate: list[dict]) -> bool:
    for i in range(0, len(candidate)-1):
       if candidate[i]["to-stop-partial"]["stop-time"]["hour"] > candidate[i+1]["from-stop-partial"]["stop-time"]["hour"]:
           return False
       
       changingTimeMins = (candidate[i+1]["from-stop-partial"]["stop-time"]["hour"] - candidate[i]["to-stop-partial"]["stop-time"]["hour"])*60 + candidate[i+1]["from-stop-partial"]["stop-time"]["minute"] - candidate[i]["to-stop-partial"]["stop-time"]["minute"]
       if(changingTimeMins < 1 or changingTimeMins > 30):
           return False
       
       
    return True

       
def passesCriteria(candidate: list[dict]) -> bool:
    fromNode:Node = database_functions.find_node_by_gtfs_id(candidate[0]["from-stop-partial"]["stop_id"])
    toNode:Node = database_functions.find_node_by_gtfs_id(candidate[-1]["to-stop-partial"]["stop_id"])
    if(is_close(fromNode, toNode)):
        return False
    if(len(candidate) > MAX_CHANGES):
        return False


    # travelTimeMins = sum([candidateMember["travelling-time-mins"] for candidateMember in candidate])
    # if(travelTimeMins > (calculate_walking_time((fromNode.latitude, fromNode.longitude), (toNode.latitude, toNode.longitude)))*2.5):
    #     return False
        
    if(not isTimingCorrect(candidate)):
        return False
    
    walking_time = calculate_walking_time((fromNode.latitude, fromNode.longitude), 
                                        (toNode.latitude, toNode.longitude))
    if walking_time > 15:  # If walking is longer than 15 minutes, allow a less strict rule
        speed_factor = 1.2  
    else:
        speed_factor = 1.5  

    if calculate_complete_time(candidate[0]["from-stop-partial"]["stop-time"], 
                            candidate[-1]["to-stop-partial"]["stop-time"]) > walking_time * speed_factor:
        return False

    
    routesAppeared = [stop['route-id'] for stop in candidate]
    if(len(set(routesAppeared)) < len(routesAppeared)):
        return False
    
    for stop in candidate:
        currentPartian = stop["from-stop-partial"]["stop_id"]
        mainSiblinbs = list(get_siblings(currentPartian)[0]["children"])
        if mainSiblinbs is not None:
            mainSiblinbs.remove(currentPartian)
            fromNodes = [from_stop["from-stop-partial"]["stop_id"] for from_stop in candidate]
            if set(mainSiblinbs).intersection(fromNodes):
                return False
        
    
    for i in range(0, len(candidate)-1):
        fromNode = candidate[i]["from-stop-partial"]
        toNode = candidate[i]["to-stop-partial"]
        nextFromNode = candidate[i+1]["from-stop-partial"]
        
        if database_functions.is_node_parent(fromNode["stop_id"]) or \
            database_functions.is_node_parent(toNode["stop_id"]):
                return False
            
        if toNode['stop_id'] != nextFromNode['stop_id'] and \
            toNode['stop_id'] not in list(database_functions.get_node_siblings(nextFromNode['stop_id']))[0]['children']:
                return False
        

    return True

def get_siblings(node: int) -> list[int]:
    if(not database_functions.is_node_parent(node)):
        return database_functions.get_node_siblings(node)
    
    return None

def get_ways_with_stop_change(node: int) -> list[int]:
    siblings = list(get_siblings(node))
    if(siblings is None):
        return []
    
    siblingList = []
    for document in siblings:
        siblingList += document.get("children", [])
    
    if(node in siblingList):
        siblingList.remove(node)
    
    return database_functions.get_solutions_with_siblings(siblingList)



async def stoplist_method_singles():
    trips = database_functions.get_all_trips() #Swao with trips -> based on time
    for trip in trips: 
        for stop in trip.stops_reached:
            pivot_list = trip.stops_reached[trip.stops_reached.index(stop) +1 : -1]
            for pair_stop in pivot_list:
                if not is_close(database_functions.find_node_by_gtfs_id(stop['stop_id']), database_functions.find_node_by_gtfs_id(pair_stop['stop_id'])):                    
                    parent = Solution_Holder(stop['stop_id'], pair_stop['stop_id'])
                    parent.addFromStopName(database_functions.get_stop_name_by_id(stop['stop_id']))
                    parent.addToStopName(database_functions.get_stop_name_by_id(pair_stop['stop_id']))
                    #Find representing edges for the stops
                    edges = database_functions.get_edges_by_stops_and_and_trip(stop['stop_id'], pair_stop['stop_id'], trip.trip_id)
                    for edge in edges:
                        #Calculate the time it takes to travel between the stops
                        route_name = database_functions.get_route_name_by_id(edge['owner-route'])
                        parent.addChange(stop, parent.fromStopName, pair_stop, parent.toStopName, edge['owner-route'], route_name,
                                         edge['travelling-time-mins'], edge['departure-time'], edge['arrival-time'])
                        if database_functions.solution_exists_in_db(stop['stop_id'], pair_stop['stop_id']):
                            database_functions.add_path_to_solution(stop['stop_id'], pair_stop['stop_id'], parent.create_inner_dict()[-1])
                        else:
                            database_functions.upload_solution(parent.to_dictionary())

                    
                    
 
print("Uploading single solutions...")       
database_functions.clear_sol()
print("Cleared")
asyncio.run(stoplist_method_singles())
print("Singles uploaded")
    

async def stoplist_method_appending():
    solutions = database_functions.get_all_solutions()
    solutionGenerated = set([solution.get_header() for solution in solutions])
    while len(solutionGenerated) > 0:
        solutions = database_functions.get_all_solutions()
        solutions = [solution for solution in solutions if solution.get_header() in solutionGenerated]
        solutionGenerated = set()
        for baseStop in solutions:
            ownStops = database_functions.get_stopSets_by_fromStop(baseStop.toStop, baseStop.getRoutes())
            siblingStops = get_ways_with_stop_change(baseStop.toStop)
            addonSources = ownStops + siblingStops
            for addonStop in addonSources:
                    for change in baseStop.changes:
                            newElement = change + addonStop
                            if passesCriteria(newElement):
                                if database_functions.solution_exists_in_db(baseStop.fromStop, addonStop[-1]['to-stop-partial']["stop_id"]):
                                    if(database_functions.add_path_to_solution(newElement[0]["from-stop-partial"]["stop_id"], newElement[-1]["to-stop-partial"]["stop_id"],newElement)):
                                        solutionGenerated.add(baseStop.get_header())
                                        solutionGenerated.add((addonStop[0]['from-stop-partial']["stop_id"],addonStop[-1]['to-stop-partial']["stop_id"]))
                                    
                                else:
                                    newSolution = Solution_Holder(newElement[0]["from-stop-partial"]["stop_id"], newElement[-1]["to-stop-partial"]["stop_id"])
                                    newSolution.addChangeDict(newElement)
                                    newSolution.addFromStopName(database_functions.get_stop_name_by_id(newElement[0]["from-stop-partial"]["stop_id"]))
                                    newSolution.addToStopName(database_functions.get_stop_name_by_id(newElement[-1]["to-stop-partial"]["stop_id"]))
                                    database_functions.upload_solution(newSolution.to_dictionary())
                                    solutionGenerated.add(baseStop.get_header())
                                    solutionGenerated.add((newElement[0]["from-stop-partial"]["stop_id"], newElement[-1]["to-stop-partial"]["stop_id"]))

print("Uploading multiples")
asyncio.run(stoplist_method_appending())
print("Multiples uploaded")

