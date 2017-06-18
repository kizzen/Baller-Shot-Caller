# -*- coding: utf-8 -*-
import json
import csv
import glob
import os
import sys
import json
import pymongo
from pprint import pprint

# 3rd party
from nba_py.constants import TEAMS
from nba_py import game
from nba_py import team
from nba_py import player
import pandas as pd

#%%#######################################################################
## establishing mongo connection, only after you get mongod.exe is running 
# C:\Program Files\MongoDB\Server\3.2\bin
##########################################################################
conn=pymongo.MongoClient()
db = conn.mydb
conn.database_names()
collection = db.PbP_Full

'''
def printJSON(your_json):
    print(json.dumps(your_json, indent=4, sort_keys=True))
'''

# Get list of game IDs for single team
def get_games_list(team_abbr='SAS'):

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


#%%#######################################################################
## Import of JSONS into mongo; not necessary to run if you already have mongo database already generated locally
##########################################################################
def pbp_toMongo():
    client = MongoClient()
    pbp_db = client['PBP']

    game_id_list = get_games_list(team_abbr)
    playbyplay_to_mongo(game_id_list, pbp_db)
        
#pprint to identify where the game events are actually present.


#%%#######################################################################
## Outputting to CSV directly from mongo. Pretty sleek yo.
##########################################################################
def outputMongo():
    cursor = collection.find({"$or":[ {"PLAYER1_TEAM_ABBREVIATION":"SAS"}, {"PLAYER2_TEAM_ABBREVIATION":"SAS"}, {"PLAYER3_TEAM_ABBREVIATION":"SAS"}]})
    def pbp_csv_to_mongo(cursor):
        with open('pbp_SAS.csv', 'a', newline='') as outfile:
            fields = ['SCORE', 'PERSON3TYPE', 'PLAYER3_NAME', 'PLAYER3_TEAM_CITY', 'VISITORDESCRIPTION', 'PLAYER1_ID', 'PERSON1TYPE', 'PERIOD', 'PLAYER1_TEAM_NICKNAME', 'HOMEDESCRIPTION', 'PLAYER1_TEAM_ID', '_id', 'WCTIMESTRING', 'PLAYER2_TEAM_NICKNAME', 'SCOREMARGIN', 'PLAYER2_NAME', 'PCTIMESTRING', 'PLAYER3_TEAM_NICKNAME', 'PLAYER1_TEAM_CITY', 'PLAYER2_ID', 'EVENTMSGTYPE', 'GAME_ID', 'PERSON2TYPE', 'EVENTNUM', 'PLAYER1_NAME', 'PLAYER3_ID', 'PLAYER3_TEAM_ABBREVIATION', 'PLAYER2_TEAM_ABBREVIATION', 'EVENTMSGACTIONTYPE', 'PLAYER3_TEAM_ID', 'PLAYER2_TEAM_CITY', 'NEUTRALDESCRIPTION', 'PLAYER2_TEAM_ID', 'PLAYER1_TEAM_ABBREVIATION']
            writer = csv.DictWriter(outfile, fieldnames=fields)
            writer.writeheader()
            for x in cursor:
                writer.writerow(x)
                
    

        