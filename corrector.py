from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient("mongodb+srv://belics_fanni:A1Yh2leQnz46L678@gtfs2023.7e1cux4.mongodb.net/?retryWrites=true&w=majority&authSource=admin")

# Replace 'yourDatabaseName' and 'yourCollectionName' with your actual database and collection names
db = client['debrecen']
collection = db['solutions']

# Iterate through each document and modify the 'changes' array
documents = collection.find({})
for doc in documents:
    filtered_changes = [change for change in doc['changes'] if len(change) == 1]
    
    # Update the document with the filtered 'changes' array
    collection.update_one(
        {'_id': doc['_id']},
        {'$set': {'changes': filtered_changes}}
    )

print("Subarrays containing more than one element have been removed from 'changes'.")
