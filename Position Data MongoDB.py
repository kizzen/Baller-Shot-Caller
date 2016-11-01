#!/usr/bin/env python

##########################################################################
## Imports
##########################################################################


import os
import glob
import json
import pymongo
from pymongo import MongoClient
import pprint


##########################################################################
## Module Variables/Constants
##########################################################################

# Set target working directory with game JSON files
# working_directory = '/media/kurt/sd/Georgetown/Game Data/Unpacked'
working_directory = '/media/kurt/KURT/Georgetown/Game Data/Spurs/'


##########################################################################
## Functions
##########################################################################


# Return list of JSON files in current working directory
def get_json_files():
    json_files = glob.glob('*.json')
    print('Found {} JSON files.'.format(len(json_files)))
    return json_files


# Open a single game JSON file and insert it as a collection of documents into a MongoDB
def create_game_collection(filename, db):

    print("Loading {} into memory".format(filename))

    # Load JSON file into memory
    with open(filename) as json_file:
        game_json = json.load(json_file)

    # Gather critical game info
    game_date = game_json['gamedate']
    game_id = game_json['gameid']
    events = game_json['events']

    # Create collection for this specific game
    collection = db[game_id]

    # Insert documents for game date and ID
    collection.insert({'game_date': game_date, 'game_id': game_id})

    events_count = 0

    # Insert the events, one at a time, as documents in the collection
    for event in events:
        print("Inserting game: {0} event: {1}".format(game_id, event['eventId']))
        collection.insert(event)
        events_count += 1

    print("Created collection: {0} events for game {1}".format(events_count, game_id))


# Loop through JSON files and insert each as a collection of event documents in db
def insert_games(json_files, db):
    current_games_count = 0
    total_games_count = len(json_files)

    print("Inserting {} games into database".format(total_games_count))

    for filename in json_files:
        current_games_count += 1
        create_game_collection(filename, db)
        print("Inserted {0} of {1} games into database".format(current_games_count, total_games_count))


# Print database names and collections
def describe_databases(client):
    d = dict((db, [collection for collection in client[db].collection_names()])
             for db in client.database_names())
    print(json.dumps(d))


##########################################################################
## Execution
##########################################################################


# Change to target working directory
os.chdir(working_directory)


# Connect to MongoDB and initialize database 'NBA'
client = MongoClient()
db = client['NBA']


# Get list of JSON files in working directory
json_files = get_json_files()


# Insert those JSON files into the database
insert_games(json_files, db)


##########################################################################
## Scratch Code
##########################################################################


# PrettyPrint syntax
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(document)


# Find first document in collection
mycursor = db[game_id].find()


# Print single document in collection
collection.find_one()
db[game_id].find_one()


# Print documents in collection (WARNING: THIS CRASHES PYTHON CONSOLE FOR ENTIRE GAME DATA)
cursor = collection.find({})
for document in cursor:
    pp.pprint(document)


# Print event IDs in collection
collection.distinct('eventId')


# Print number of documents in collection
collection.count()


# Drop database NBA
client.drop_database('NBA')


# sudo service mongod start --dbpath /media/kurt/sd/MongoDB/db
# sudo mongod --dbpath /media/kurt/sd/MongoDB/db