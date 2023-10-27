from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os,sys, path

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from graph_elements.node import Node

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()


connection_string=f"mongodb+srv://belics_fanni:{PASSWORD}@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

database = client[DICTIONARY]

def to_dictionary(node: Node) -> dict:
    data = {
            "gtfs-id": int(node.gtfs_id),
            "name": node.name,
            "short-name": node.short_name,
            "description": node.description,
            "longitude" : float(node.longitude),
            "latitude" : float(node.latitude)
        }
    if node.parental_node != None: 
        data.update({"parental-node" : int(node.parental_node)})
        
    if len(node.children) > 0:
        li = list(node.children)
        data.update({"children" : li})
        
    return data

def to_node(candidate: dict) -> Node:
    node = Node()
    node.gtfs_id = candidate["gtfs-id"]
    node.name = candidate["name"]
    node.short_name = candidate["short-name"]
    node.description = candidate["description"]
    node.longitude = candidate["longitude"]
    node.latitude = candidate["latitude"]
    if "parental-node" in candidate.keys:
        node.parental_node = candidate["parental-node"]
    else:
        node.parental_node = None
        
    if "children" in candidate.keys:
        node.children = candidate["children"]
    else:
        node.children = []
        
    return node
    

def upload_node_to_database(node: Node) -> bool:
    data = to_dictionary(node)
    try:
        database[NODES_COLLECTION].insert_one(data)
        
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

def find_node_by_gtfs_id(gtfs_id: int) -> Node: 
    return database[NODES_COLLECTION].find_one({'gtfs-id': gtfs_id})
