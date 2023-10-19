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

def create_dictionary_proper_types(node: Node) -> dict:
    data = {
            "gtfs-id": int(node.gtfs_id),
            "name": node.name,
            "description": node.description,
            "longitude" : float(node.longitude),
            "latitude" : float(node.latitude)
        }
    return data

def upload_node_to_database(node: Node) -> bool:
    data = create_dictionary_proper_types(node)
    try:
        database[NODES_COLLECTION].insert_one(data)
        
    except Exception as e:
        print(e)
        return False
    
    else:
        return True

    