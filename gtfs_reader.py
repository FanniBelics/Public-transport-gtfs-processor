# -*- coding: utf-8 -*-

import os
from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip
from graph_elements.edge import Edge
import database_management.database_functions as database_functions
from dotenv import load_dotenv, find_dotenv
import os
import csv

absolute_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
load_dotenv(find_dotenv())
gtfs_path = os.environ.get("READ_DICTIONARY")
full_path = os.path.join(absolute_path, gtfs_path)

def existing_location(nodeCandidate: Node, nodesList: list[Node]) -> bool:
    for node in nodesList:
        if node.gtfs_id != nodeCandidate.gtfs_id and node == nodeCandidate:
            return True
        return False

def read_stops(): 
    """Method to read the stops.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
        Uses the csv.reader from module csv\n
    """
    
    with open (full_path + "/stops.txt", encoding="utf-8") as stops_txt:
        for stop in csv.reader(stops_txt):
            if stop[0] != "stop_id":
                newNode = Node(stop[0],stop[1],stop[2],stop[3],stop[7],stop[6])
                database_functions.upload_node_to_database(newNode)
                if stop[9] != '':
                    newNode.set_parental_node(database_functions.find_node_by_gtfs_id(stop[9]))
                    database_functions.add_parental_node_to_node(newNode, stop[9])
                    database_functions.add_child_to_node(stop[9], newNode.gtfs_id)

def read_routes():
    """Method to read the routes.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
        Uses the csv.reader from module csv\n
    """
    with open(full_path + "/routes.txt", encoding="utf-8") as routes_txt:
        for route in csv.reader(routes_txt):
            if route[0] != "route_id":
                newRoute = Route(route[0], route[1], route[3], route[5])
                newRoute.add_long_name(route[4])
                newRoute.add_route_type(route[2])
                database_functions.upload_route_to_database(newRoute)
                
def read_trips():
    """Method to read the trips.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
        Uses the csv.reader from module csv\n
    """
    with open(full_path + "/trips.txt", encoding="utf-8") as trips_txt:
        for trip in csv.reader(trips_txt):
            if trip[0] != "trip_id":
                newTrip = Trip(trip[0], trip[1], trip[2],trip[5])
                newTrip.add_direction(trip[3])
                database_functions.upload_trip_to_database(newTrip)
                database_functions.add_trip_to_route(trip[1],trip[0])
                
def read_stop_times():
    with open(full_path + "/stop_times.txt", encoding="utf-8") as stop_times:
        oldEdge = Edge(0,0,0)
        for stop_time in csv.reader(stop_times):
            #Saving stop reaching to trip
            if stop_time[0] != "trip_id":
                
                id = stop_time[0] + "_" + stop_time[1]
                newEdge = Edge(id, oldEdge.toStop, stop_time[2])
                newEdge.set_departure_time(stop_time[5])
                newEdge.set_owner_trip(int(stop_time[0]))
                newEdge.set_distance(int(stop_time[8]), oldEdge.distance)
                
                if stop_time[8] == "0":
                    trip = database_functions.find_trip_by_id(int(stop_time[0]))
                    route = database_functions.find_route_by_id(trip.route_id)
                    newEdge.set_owner_route(route.route_id)
                    newEdge.set_arrival_time(stop_time[4])
                    
                else:
                    newEdge.set_arrival_time(oldEdge.get_departure_time)
                    newEdge.set_owner_route(route.route_id)
                    newEdge.set_travelling_time(stop_time[4], oldEdge.get_departure_time())
                    #database_functions.upload_edge_to_database(newEdge)
                
                oldEdge = newEdge
                trip.add_reached_stop(stop_time[2], stop_time[5])
                route.add_stop(stop_time[2])
                #database_functions.add_stop_to_route(route.route_id, stop_time[2]) #does same don't touch db yet
                #database_functions.add_stop_to_trip(trip.trip_id, trip.stops_reached[-1]) #does same don't touch db yet
                print(trip.trip_id, trip.stops_reached[-1])

        
read_stop_times()