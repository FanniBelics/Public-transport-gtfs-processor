from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip
from graph_elements.edge import Edge
from itertools import combinations
import database_management.database_functions as database_functions
import asyncio

STOPS = database_functions.get_all_stops()

async def async_range(start, stop=None, step=1):
    if stop:
        range_ = range(start, stop, step)
    else:
        range_ = range(start)
    for i in range_:
        yield i
        await asyncio.sleep(0)

def is_close(first_stop: Node, second_stop: Node):
    if first_stop == second_stop:
        return True
    
    
    walk_speed = 5 #The average walking speed understood in km/h
    distance = first_stop.calculate_dist(second_stop)
    return round((distance / walk_speed)*60) <= 2 #the time it takes to walk the distance
       
async def find_paired_stops():
    global transport_pairs #These are stops that are close enough to each other that one can literally walk there 
    transport_pairs = [(stop1.gtfs_id, stop2.gtfs_id) for stop1, stop2 in combinations(STOPS, 2)
                       if is_close(stop1, stop2) and database_functions.is_stop_on_same_route(stop1, stop2)]
    
            
#asyncio.run(find_paired_stops())

async def define_pairs():
    global pairs_to_find 
    pairs_to_find = [(stop1.gtfs_id, stop2.gtfs_id) for stop1, stop2 in combinations(STOPS,2)
                     if (stop1.gtfs_id, stop2.gtfs_id) not in transport_pairs]
    
#asyncio.run(define_pairs())    

async def write_to_file():
    with open("transport_pairs.csv", 'w') as f:
        oldp1 = ""
        for p1, p2 in transport_pairs:
            if oldp1 != p1:
                f.write("\n")
            f.write("( {0}, {1});".format(p1,p2))
            oldp1 = p1
            
        
    with open("pairs_to_find.csv", 'w') as f:
        oldp1 = ""
        for p1, p2 in pairs_to_find:
            if oldp1 != p1:
                f.write("\n")
            f.write("( {0}, {1});".format(p1,p2))
            oldp1 = p1
        
#asyncio.run(write_to_file())

async def stoplist_method():
    MAX_CHANGES = 1
    for stop in STOPS:
        stoplist = []
        route = database_functions.find_routes_by_stop_id(stop.gtfs_id)
        if not len(route):
            continue
        print(f"{route}")
        
asyncio.run(stoplist_method())