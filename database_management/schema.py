node_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title" : "Schema for Node object validation",
        "required" : ["gtfs-id", "name", "longitude", "latitude"],
        "properties" : {
            "gtfs-id" : {
                "bsonType" : "int",
                "description" : "GTFS id of given stop and is required"
             },
            "name" : {
                "bsonType" : "string",
                "description" : "Name of given stop and is required"
            },
            "description":{
                "bsonType" : "string",
                "description" : "Short description of the given stop"
                },
            "longitude " : {
                "bsonType" : "double",
                "description" : "Longitude element of the stop and is required",
                "minimum": -180.0,
                "maximum": 180.0
            },
            "latitude" : {
                "bsonType" : "double",
                "description" : "Latitude of given stop and is required",
                "minimum" : -90.0,
                "maximum" : 90.0
            }
        }
    }
}

edge_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title": "Schema for Edge schema validation",
        "required" : ["id", "fromNodeId", "toNodeId", "distance"],
        "properties" : {
            "id" : {
                "bsonType" : "int",
                "description": "Id of the way from one stop to another on one route"
            },
            "fromNodeId" : {
                "bsonType" : "int",
                "description" : "Node id of the node the edge starts from"
            },
            "toNodeId" : {
                "bsonType" : "int",
                "description" : "Node id of the node the edge goes to"
            },
            "distance": {
                "bsonType" : "double",
                "description" : "The distane between nodes defined in fromNodeId and toNodeId",
                "minimum" : 0.0
            } 
        }
    }
}