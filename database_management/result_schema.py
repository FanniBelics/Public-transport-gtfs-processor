result_schema = {
    "$jsonSchema" : {
        "bsonType" : "object",
        "title" : "Schema for validating results",
        "required" : ["from-id", "to-id"],
        "properties" : {
            "from-id" : {
                "bsonType" : "int",
                "description" : "The stop-id of the starting stop"
            },
            "from-name" : {
                "bsonType" : "string",
                "description" : "The name of the starting stop"
            },
            "to-id" : {
                "bsonType" : "int",
                "description" : "The stop-id of the final stop"
            },
            "to-name" : {
                "bsonType" : "string",
                "description" : "The name of the final stop"
            },
            "changes" : {
                "bsonType" : "array",
                "uniqueItems" : True,
                "items" : {
                        "bsonType": "array",
                        "uniqueItems" : True,
                        "items" : {
                            "bsonType" : "object",
                            "properties" : 
                                {
                                "from-stop-partial" : {
                                "bsonType" : "object",
                                "properties" : {
                                    "stop_id": {
                                        "bsonType": "int"
                                    },
                                    "stop-name": {
                                        "bsonType": "string"
                                    },
                                    "stop-time": {
                                        "bsonType": "object",
                                        "properties":{
                                            "hour": {
                                                "bsonType": "int"
                                            },
                                            "minute": {
                                                "bsonType": "int"
                                            },
                                            "second": {
                                                "bsonType": "int"
                                            }
                                        }
                                    }
                                }
                                },
                                "to-stop-partial" : {
                                "bsonType" : "object",
                                "properties" : {
                                    "stop_id": {
                                        "bsonType": "int"
                                    },
                                    "stop-name": {
                                        "bsonType": "string"
                                    },
                                    "stop-time": {
                                        "bsonType": "object",
                                        "properties":{
                                            "hour": {
                                                "bsonType": "int"
                                            },
                                            "minute": {
                                                "bsonType": "int"
                                            },
                                            "second": {
                                                "bsonType": "int"
                                            }
                                        }
                                    }
                                }
                                
                                },
                                "route-id" : {
                                "bsonType" : "int"
                                 },
                                "route-name" : {
                                "bsonType" : "string"
                                },
                        }
                    }
                }
            }
        }
    }
}