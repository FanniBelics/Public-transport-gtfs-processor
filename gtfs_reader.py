# -*- coding: utf-8 -*-

import os
from graph_elements.node import Node
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

def read_nodes():
    with open (full_path + "/stops.txt", encoding="utf-8") as stops_txt:
        for stop in csv.reader(stops_txt):
            if stop[0] != "stop_id":
                newNode = Node(stop[0],stop[1],stop[2],stop[3],stop[7],stop[6])
                database_functions.upload_node_to_database(newNode)
                if stop[9] != '':
                    newNode.set_parental_node(database_functions.find_node_by_gtfs_id(stop[9]))
                    database_functions.add_parental_node_to_node(newNode, stop[9])
                    database_functions.add_child_to_node(stop[9], newNode.gtfs_id)

read_nodes()
