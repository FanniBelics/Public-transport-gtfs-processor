from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from schema import node_schema, edge_schema, route_schema
import os
import sys

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
ROUTES_COLLECTION = os.environ.get("COLLECTION_ROUTES_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()


connection_string=f"mongodb+srv://belics_fanni:{PASSWORD}@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

database = client[DICTIONARY]
try:
    nodesCollection = database.create_collection(NODES_COLLECTION)
except Exception:
    print("Collection already exists")
    coll = database[NODES_COLLECTION]
finally:
    database.command("collMod",NODES_COLLECTION, validator = node_schema)
    
try:
    edgesCollection = database.create_collection(EDGES_COLLECTION)
except Exception:
    print("Collection already exists")
    coll = database[EDGES_COLLECTION]
finally:
    database.command("collMod",EDGES_COLLECTION, validator = edge_schema)
    
try:
    edgesCollection = database.create_collection(ROUTES_COLLECTION)
except Exception:
    print("Collection already exists")
    coll = database[ROUTES_COLLECTION]
finally:
    database.command("collMod",ROUTES_COLLECTION, validator = route_schema)
    