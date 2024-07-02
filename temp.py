from pymongo import MongoClient


mongo_connection_string = "mongodb://localhost:27017"
client = MongoClient(mongo_connection_string)

db = client.questions_db
buffer_collection = db.buffer


match = [1,3,11]
result = list(buffer_collection.find({"Key":{"$eq":1}}))[0]

print(result)
# for document in result:
#     print(document)