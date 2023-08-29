# -*- coding: utf-8 -*-

from pymongo import MongoClient
import os
from graph_elements.node import Node
import csv

absolute_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
gtfs_path = "gtfs-debrecen"
full_path = os.path.join(absolute_path, gtfs_path)


#with open (full_path + "/agency.txt", encoding="utf-8") as ageny_txt:
#    print(ageny_txt.read())

with open (full_path + "/stops.txt", encoding="utf-8") as stops_txt:
    nodes = set()
    for stop in csv.reader(stops_txt):
       if stop[0] != "id":
           newNode = Node(stop[0],stop[1],stop[7],stop[6])
           nodes.add(newNode)
           print(newNode)