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
    transport_pairs = [(stop1.name, stop2.name) for stop1, stop2 in combinations(STOPS, 2)
                       if is_close(stop1, stop2) and database_functions.is_stop_on_same_route(stop1, stop2)]
    
    print(transport_pairs)
            
asyncio.run(find_paired_stops())

def define_pairs():
    pass