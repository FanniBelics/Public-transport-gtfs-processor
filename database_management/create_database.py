from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import schema as schemas
import os
import sys

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PSW")
NODES_COLLECTION = str(os.environ.get("COLLECTION_NODE_NAME"))
EDGES_COLLECTION = os.environ.get("COLLECTION_EDGE_NAME")
ROUTES_COLLECTION = os.environ.get("COLLECTION_ROUTES_NAME")
TRIPS_COLLECTION = os.environ.get("COLLECTION_TRIPS_NAME")
DICTIONARY = os.environ.get("READ_DICTIONARY").lower()

connection_string=f"mongodb+srv://belics_fanni:{PASSWORD}@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(connection_string)

database = client[DICTIONARY]

#database.drop_collection(NODES_COLLECTION)
#database.drop_collection(TRIPS_COLLECTION)
#database.drop_collection(ROUTES_COLLECTION)

try:
    database.create_collection(NODES_COLLECTION)
except Exception:
    print("Collection already exists")
finally:
    database.command("collMod",NODES_COLLECTION, validator = schemas.node_schema)
    
try:
    database.create_collection(EDGES_COLLECTION)
except Exception:
    print("Collection already exists")
finally:
    database.command("collMod",EDGES_COLLECTION, validator = schemas.edge_schema)
    
try:
    database.create_collection(ROUTES_COLLECTION)
except Exception:
    print("Collection already exists")
finally:
    database.command("collMod",ROUTES_COLLECTION, validator = schemas.route_schema)
    
try:
    database.create_collection(TRIPS_COLLECTION)
except Exception:
    print("Collection already exists")
finally:
    database.command("collMod",TRIPS_COLLECTION, validator = schemas.trip_schema)