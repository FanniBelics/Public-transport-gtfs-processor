node_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title" : "Schema for Node object validation",
        "required" : ["gtfs-id", "name", "short-name","longitude", "latitude"],
        "properties" : {
            "gtfs-id" : {
                "bsonType" : "int",
                "description" : "GTFS id of given stop and is required"
             },
            "name" : {
                "bsonType" : "string",
                "description" : "Full name of given stop and is required"
            },
            "short-name":{
                "bsonType" : "string",
                "description" : "Short name of given stop and is required"
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
            },
            "parental-node" : {
                "bsonType" : "int",
                "description" : "The parental node of the current stop"
            },
            "children" : {
                "bsonType" : "array", 
                "uniqueItems": True,
                "items" : {
                    "bsonType" : "int"
                },
                "description" : "The children of the current stop, identified by the their gtfs-id"
            },
            "routes" : {
                "bsonType" : "array",
                "uniqueItems" : True,
                "items" :  {
                    "bsonType" : "int"
                },
                "description" : "All the routes, that reaches the current stop"
            }
        }
    }
}

edge_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title": "Schema for Edge schema validation",
        "required" : ["id", "from-stop", "to-stop", "distance"],
        "properties" : {
            "id" : {
                "bsonType" : "int",
                "description": "Id of the way from one stop to another on one route"
            },
            "from-stop" : {
                "bsonType" : "int",
                "description" : "Stop id of the node the edge starts from"
            },
            "to-stop" : {
                "bsonType" : "int",
                "description" : "Stop id of the node the edge goes to"
            },
            "distance": {
                "bsonType" : "double",
                "description" : "The distane between nodes defined in fromNodeId and toNodeId, in meters",
                "minimum" : 0.0
            },
            "travelling-time-mins" : {
                "bsonType" : "int",
                "description" : "Travelling time in minutes, without seconds",
                "minimum" : 0
            },
            "travelling-time-secs" : {
                "bsonType" : "int",
                "description" : "Travelling time in seconds, without minutes",
                "minimum" : 0,
                "maximum" : 60
            },
            "departure-time" : {
                "bsonType" : "object",
                "description" : "The time the travel starts from the current stop",
                "properties" : {
                           "hour" : {
                               "bsonType" : "int",
                               "minimum" : 0
                           },
                           "minute" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           },
                           "second" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           }
                       }
            },
            "arrival-time" : {
                "bsonType" : "object",
                "description" : "The time the vehicle arrives to the following stop",
                "properties" : {
                           "hour" : {
                               "bsonType" : "int",
                               "minimum" : 0
                           },
                           "minute" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           },
                           "second" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           }
                       }
            },
            "owner-trip" : {
                "bsonType" : "int",
                "description" : "The trip that specifies this transportation between two stops"
            },
            "owner-route" : {
                "bsonType" : "int",
                "description" : "The route that the current transportation belongs to"
            }
        }
    }
}

route_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title": "Schema for routes schema validation",
        "required" : ["route-id", "agency-id", "route-type", "route-short-name", "route-description"],
        "properties" : {
            "route-id" : {
                "bsonType" : "int",
                "description" : "Original route_id given from GTFS files"
            },
            "agency-id" : {
                "bsonType" : "string",
                "description" : "Identifies the agency, the route belongs to"
            },
            "route-type" : {
                "bsonType" : "int",
                "description" : "Identifies the mean of the transportation",
                "enum" : [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 800]
            },
            "route-type-as-text" : {
                "bsonType" : "string",
                "description" : "Identifies the name of mean of transportation, default language EN"
            },
            "route-short-name" : {
                "bsonType" : "string",
                "description" : "Short name of the route"
            },
            "route-long-name" : {
                "bsonType" : "string",
                "description" : "Full name of the route, if none same as the short name"
            },
            "route-description" : {
                "bsonType" : "string",
                "description" : "Description of the route"
            },
            "stops-reached" : {
                "bsonType" : "array",
                "uniqueItems" : True,
                "items": {
                    "bsonType" : "int"
                },
                "description" : "Array of the stops, the specified route touches"
            },
            "trips" : {
                "bsonType" : "array",
                "uniqueItems" : True,
                "items": {
                    "bsonType" : "int"
                },
                "description" : "Array of the trips in the current route"
            }
        }
    }
}

trip_schema = {
   "$jsonSchema" : {
       "bsonType" : "object",
       "title" : "Schema for validating trips",
       "required" : ["trip-id", "route-id", "service-id"],
       "properties" : {
           "trip-id" : {
               "bsonType" : "int",
               "description" : "The id given in GTFS files for the current trip"
           },
           "route-id" : {
               "bsonType" : "int",
               "description" : "Foreign key to the route owning the current stop"
           },
           "service-id" : {
               "bsonType" : "string",
               "description" : "Foreign key to identify the service"
           },
           "direction-id" : {
               "bsonType" : "int",
               "description" : "Identifies the direction",
               "enum" : [0,1]
           },
           "opposite-direction" : {
               "bsonType" : "bool",
               "description" : "Calculated from the direction-id, identifies if the trip is going the opposite direction"
           },
           "trip-headsign" : {
               "bsonType" : "string",
               "description" : "Text that appears on signage identifying the trip's destination to riders"
           },
           "stops-reached" : {
               "bsonType" : "array",
               "description" : "Sequence of stops reached in each trip",
               "items" : {
                   "stop-id" : {
                       "bsonType" : "int"
                   },
                   "stop_time" : {
                       "bsonType" : "object",
                       "properties" : {
                           "hour" : {
                               "bsonType" : "int",
                               "minimum" : 0
                           },
                           "minute" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           },
                           "second" : {
                               "bsonType" : "int",
                               "minimum" : 0,
                               "maximum" : 60
                           }
                       }
                       
                   }
               }
           }
       } 
   }
}