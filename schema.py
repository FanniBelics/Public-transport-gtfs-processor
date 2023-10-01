node_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title" : "Schema for Node object validation",
        "required" : ["id", "name", "longitude", "latitude"],
        "properties" : {
            "gtfs-id" : {
                "bsonType" : "int",
                "description" : "GTFS id of given stop and is required"
             },
            "name" : {
                "bsonType" : "string",
                "description" : "Name of given stop and is required"
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
            },
            "aliases" : {
                "bsonType" : ["int"],
                "description" : "Other ids for the same node, if exists" 
            }
        }
    }
}

edge_schema = {
    "$jsonSchema" : {
        
    }
}