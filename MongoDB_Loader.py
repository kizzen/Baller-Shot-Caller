
#Python Script to load single Game events from single JSON file to MongoDB

import json
import pymongo
from pprint import pprint
conn=pymongo.MongoClient()
db = conn.mydb
conn.database_names()
collection = db.my_collection
db.collection_names()
with open("0021500001.json") as data_file:
    noaa = json.load(data_file)

events= noaa["events"]
collection.insert(events)

print()

#db.close()
