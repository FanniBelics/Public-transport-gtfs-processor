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
            "to-id" : {
                "bsonType" : "int",
                "description" : "The stop-id of the final stop"
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
                                "bsonType" : "int"
                                },
                                "to-stop-partial" : {
                                "bsonType" : "int"
                                },
                                "route-id" : {
                                "bsonType" : "int"
                            }
                        }
                    }
                }
            }
        }
    }
}