from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip
from graph_elements.edge import Edge
import database_management.database_functions as database_functions

STOPS = database_functions.get_all_stops()

print(STOPS)

def find_paired_stops():
    pass

def define_pairs():
    pass