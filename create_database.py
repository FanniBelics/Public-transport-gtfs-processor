from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from schema import node_schema
import os
import sys

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()


connection_string=f"mongodb+srv://belics_fanni:{PASSWORD}@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

database = client[DICTIONARY]
try:
    coll = database.create_collection(NODES_COLLECTION)
except Exception:
    print("Collection already exists")
    coll = database[NODES_COLLECTION]
finally:
    database.command("collMod",NODES_COLLECTION, validator = node_schema)
    
