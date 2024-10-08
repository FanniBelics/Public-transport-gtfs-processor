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
    return round((distance / WALK_SPEED)*60) <= 2 #the time it takes to walk the distance

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


       
def passesCriteria(candidate: list[dict]) -> bool:
    fromNode:Node = database_functions.find_node_by_gtfs_id(candidate[0]["from-stop-partial"])
    toNode:Node = database_functions.find_node_by_gtfs_id(candidate[-1]["to-stop-partial"])
    if(is_close(fromNode, toNode)):
        return False
    if(len(candidate) > MAX_CHANGES):
        return False
    
    travelTimeMins = sum([candidateMember["travelling-time-mins"] for candidateMember in candidate])
    if(travelTimeMins > (calculate_walking_time((fromNode.latitude, fromNode.longitude), (toNode.latitude, toNode.longitude)))*2.5):
        return False
    
    routesAppeared = [stop['route-id'] for stop in candidate]
    if(len(set(routesAppeared)) < len(routesAppeared)):
        return False
    
    for i in range(0, len(candidate)-1):
        fromNode = candidate[i]["from-stop-partial"]
        toNode = candidate[i]["to-stop-partial"]
        nextFromNode = candidate[i+1]["from-stop-partial"]
        
        if database_functions.is_node_parent(fromNode) or \
            database_functions.is_node_parent(toNode):
                return False
            
        if toNode != nextFromNode and \
            toNode not in list(database_functions.get_node_siblings(nextFromNode))[0]['children']:
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
    routes = database_functions.get_all_routes()
    for route in routes: 
        for stop in route.stops:
            pivot_list = route.stops[route.stops.index(stop) +1 : -1]
            for pair_stop in pivot_list:
                if not is_close(database_functions.find_node_by_gtfs_id(stop), database_functions.find_node_by_gtfs_id(pair_stop)):
                    stopsBetween = route.stops[route.stops.index(stop): route.stops.index(pair_stop)+1]
                    
                    parent = Solution_Holder(stop, pair_stop)
                    travelling_time = 0
                    for i in range(len(stopsBetween)-1):
                        transfertimes = database_functions.get_edge_transferTimes(stopsBetween[i], stopsBetween[i+1])
                        if(len(transfertimes) > 0):
                            travelling_time += round(mean([time["travelling-time-mins"] + time["travelling-time-secs"]/60 
                                        for time in transfertimes]))
                        else:
                            travelling_time = 2
                    parent.addChange(stop, pair_stop, route.route_id, travelling_time)
                    if database_functions.solution_exists_in_db(stop, pair_stop):
                        database_functions.add_path_to_solution(stop, pair_stop, parent.create_inner_dict()[-1])
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
                                if database_functions.solution_exists_in_db(baseStop.fromStop, addonStop[-1]['to-stop-partial']):
                                    if(database_functions.add_path_to_solution(newElement[0]["from-stop-partial"], newElement[-1]["to-stop-partial"],newElement)):
                                        solutionGenerated.add(baseStop.get_header())
                                        solutionGenerated.add((addonStop[0]['from-stop-partial'],addonStop[-1]['to-stop-partial']))
                                    
                                else:
                                    newSolution = Solution_Holder(newElement[0]["from-stop-partial"], newElement[-1]["to-stop-partial"])
                                    newSolution.addChangeDict(newElement)
                                    database_functions.upload_solution(newSolution.to_dictionary())
                                    solutionGenerated.add(baseStop.get_header())
                                    solutionGenerated.add((newElement[0]["from-stop-partial"], newElement[-1]["to-stop-partial"]))

print("Uploading multiples")
#asyncio.run(stoplist_method_appending())
print("Multiples uploaded")

