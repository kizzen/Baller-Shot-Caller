#!/usr/bin/env python

# Script to gather play-by-play data for a single season into MongoDB\

# NOTE: My local instance of nba_py has been modified to query the 2015-16 season explicitly


##########################################################################
## Imports
##########################################################################


import json
from nba_py.constants import TEAMS
from nba_py import game
from nba_py import team
from nba_py import player
import pandas as pd
from pymongo import MongoClient


##########################################################################
## Module Variables/Constants
##########################################################################

# We want the Spurs.
team_abbr = 'SAS'

##########################################################################
## Functions
##########################################################################

'''
def printJSON(your_json):
    print(json.dumps(your_json, indent=4, sort_keys=True))
'''

# Get list of game IDs for single team
def get_games_list(team_abbr):

    gamelogs = team.TeamGameLogs(team_id=TEAMS[team_abbr]['id']).json

    headers = gamelogs['resultSets'][0]['headers']

    games_playbyplay = gamelogs['resultSets'][0]['rowSet']

    game_id_list = []

    for single_game in games_playbyplay:
        game_id = single_game[1]
        game_id_list.append(game_id)

    return game_id_list

# Insert play-by-play data for list of games into MongoDB database
def playbyplay_to_mongo(game_id_list, pbp_db):

    for game_id in game_id_list:
        playbyplay = game.PlayByPlay(game_id).json
        collection = pbp_db[game_id]
        collection.insert(playbyplay)


# Print database names and collections
def describe_databases(client):
    d = dict((db, [collection for collection in client[db].collection_names()])
             for db in client.database_names())
    print(json.dumps(d))

# Print collections for single db
def describe_collections(db):
    d = db.collection_names()
    print(json.dumps(d))


##########################################################################
## Execution
##########################################################################


client = MongoClient()
pbp_db = client['PBP']

game_id_list = get_games_list(team_abbr)
playbyplay_to_mongo(game_id_list, pbp_db)


##########################################################################
## Scratch
##########################################################################


# The following is scratch code used in development. It is not used in the actual execution.

'''
game_id = game_id_list[0]
game_pbp = pbp_db[game_id]
cursor = game_pbp.find({})
for document in cursor:
    print(document)


# PrettyPrint syntax
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(document)

'''
