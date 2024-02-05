# -*- coding: utf-8 -*-

from graph_elements.node import Node
from graph_elements.route import Route
from graph_elements.trip import Trip
from graph_elements.edge import Edge
import database_management.database_functions as database_functions
from dotenv import load_dotenv, find_dotenv
import os
import csv
import asyncio

import aiofiles
from aiocsv import AsyncDictReader

absolute_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
load_dotenv(find_dotenv())
gtfs_path = os.environ.get("READ_DICTIONARY")
full_path = os.path.join(absolute_path, gtfs_path)

def existing_location(nodeCandidate: Node, nodesList: list[Node]) -> bool:
    for node in nodesList:
        if node.gtfs_id != nodeCandidate.gtfs_id and node == nodeCandidate:
            return True
        return False

async def read_stops(): 
    """Method to read the stops.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
    """
    
    async with aiofiles.open (full_path + "/stops.txt", encoding="utf-8") as stops_txt:
        async for stop in AsyncDictReader(stops_txt, delimiter = ","):
            newNode = Node(stop["stop_id"],stop["stop_name"],stop["stop_shortname"],stop["stop_desc"],stop["stop_lon"],stop["stop_lat"])
            database_functions.upload_node_to_database(newNode)
            if stop["parent_station"] != '':
                newNode.set_parental_node(database_functions.find_node_by_gtfs_id(stop["parent_station"]))
                database_functions.add_parental_node_to_node(newNode, stop["parent_station"])
                database_functions.add_child_to_node(stop["parent_station"], newNode.gtfs_id)

#asyncio.run(read_stops()) #run when creating a new database 

async def read_routes():
    """Method to read the routes.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
    """
    async with aiofiles.open(full_path + "/routes.txt", encoding="utf-8") as routes_txt:
        async for route in AsyncDictReader(routes_txt, delimiter = ","):
            newRoute = Route(route["route_id"], route["agency_id"], route["route_short_name"], route["route_desc"])
            newRoute.add_long_name(route["route_long_name"])
            newRoute.add_route_type(route["route_type"])
            database_functions.upload_route_to_database(newRoute)


#asyncio.run(read_routes()) #run when creating new database
                
async def read_trips():
    """Method to read the trips.txt file and load it's content into the database\n
        Expects the file to be encoded in utf-8\n
        Reads automatically from the library using the full path and the file name\n
    """
    async with  aiofiles.open(full_path + "/trips.txt", encoding="utf-8") as trips_txt:
        async for trip in AsyncDictReader(trips_txt):
            newTrip = Trip(trip["trip_id"], trip["route_id"], trip["service_id"],trip["trip_headsign"])
            newTrip.add_direction(trip["direction_id"])
            database_functions.upload_trip_to_database(newTrip)
            database_functions.add_trip_to_route(trip["route_id"],trip["trip_id"])
            
#asyncio.run(read_trips()) #run when creating new database
                
def read_stop_times():
    with open(full_path + "/stop_times.txt", encoding="utf-8") as stop_times:
        oldEdge = Edge(0,0,0)
        for stop_time in csv.reader(stop_times):
            if stop_time[0] != "trip_id":
                
                id = stop_time[0] + "_" + stop_time[1]
                newEdge = Edge(id, oldEdge.toStop, stop_time[2])
                newEdge.set_departure_time(stop_time[5])
                newEdge.set_owner_trip(int(stop_time[0]))
                
                
                if stop_time[8] == "0":
                    trip = database_functions.find_trip_by_id(int(stop_time[0]))
                    route = database_functions.find_route_by_id(trip.route_id)
                    newEdge.set_owner_route(route.route_id)
                    newEdge.set_arrival_time(stop_time[4])
                    newEdge.set_distance(0,0)
                    
                else:
                    newEdge.set_arrival_time(oldEdge.get_departure_time())
                    newEdge.set_owner_route(route.route_id)
                    newEdge.set_travelling_time(stop_time[4], oldEdge.get_departure_time())
                    newEdge.set_distance(int(stop_time[8]), oldEdge.distance)
                    database_functions.upload_edge_to_database(newEdge)
                
                oldEdge = newEdge
                trip.add_reached_stop(stop_time[2], stop_time[5])
                route.add_stop(stop_time[2])
                database_functions.add_stop_to_route(route.route_id, stop_time[2])
                database_functions.add_stop_to_trip(trip.trip_id, trip.stops_reached[-1])

read_stop_times()