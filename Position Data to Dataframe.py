#!/usr/bin/env python

# Script to convert game event ID stored in MongoDB to Pandas dataframe for analysis

# TODO: Visualize each event as an image, potentially?


##########################################################################
## Imports
##########################################################################

import json
import pprint
import pandas as pd
import numpy as np
from pymongo import MongoClient

##########################################################################
## Module Variables/Constants
##########################################################################


client = MongoClient()
nba_db = client['NBA']
pbp_db = client['PBP']


##########################################################################
## Functions
##########################################################################


# Print database names and collections
def describe_databases(client):
    d = dict((db, [collection for collection in client[db].collection_names()])
             for db in client.database_names())
    print(json.dumps(d))


# Transform a JSON event into a Pandas dataframe
def event_to_df(event, event_id, game_date, game_id):

    home = event['home']
    visitor = event['visitor']
    moments = event['moments']

    # Column labels
    headers = ["team_id", "player_id", "x_loc", "y_loc", "radius", "moment",
               "game_clock", "shot_clock", "event_id", "game_date", "game_id", "home_description",
               "neutral_description", "visitor_description", "period", "event_game_clock", "score",
               "score_margin", "event_msg_type", "event_msg_action_type"]

    # Initialize our new list
    player_moments = []

    # Gather play-by-play data for this event
    pbp_headers = ['GAME_ID', 'EVENTNUM', 'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE',
                   'PERIOD', 'WCTIMESTRING', 'PCTIMESTRING', 'HOMEDESCRIPTION',
                   'NEUTRALDESCRIPTION', 'VISITORDESCRIPTION', 'SCORE', 'SCOREMARGIN']

    # Call the PBP database for play-by-play information about the current event
    pbp_data = pbp_db[game_id].find_one()
    events_list = pbp_data['resultSets'][0]['rowSet']
    event_info = events_list[int(event_id)]
    event_dict = dict(zip(pbp_headers, event_info))

    for moment in moments:

        # For each player/ball in the list found within each moment
        for player in moment[5]:

            # Add additional information to each player/ball
            # This info includes the index of each moment, the game clock
            # and shot clock values for each moment
            player.extend((moments.index(moment), moment[2], moment[3], event_id,
                           game_date, game_id, event_dict['HOMEDESCRIPTION'],
                           event_dict['NEUTRALDESCRIPTION'], event_dict['VISITORDESCRIPTION'],
                           event_dict['PERIOD'], event_dict['PCTIMESTRING'], event_dict['SCORE'],
                           event_dict['SCOREMARGIN'], event_dict['EVENTMSGTYPE'],
                           event_dict['EVENTMSGACTIONTYPE']))

            player_moments.append(player)

    # creates the players list with the home players
    players = home["players"]

    # Then add on the visiting players
    players.extend(visitor["players"])

    # initialize new dictionary
    id_dict = {}

    # Add the values we want
    for player in players:
        id_dict[player['playerid']] = [player["firstname"] + " " + player["lastname"],
                                       player["jersey"]]

    # Add the ball to the id_dict
    id_dict.update({-1: ['ball', np.nan]})

    # create the DataFrame
    df = pd.DataFrame(player_moments, columns=headers)

    df["player_name"] = df.player_id.map(lambda x: id_dict[x][0])

    # Do not need player jersey number for now. This may be needlessly computationally expensive.
    # df["player_jersey"] = df.player_id.map(lambda x: id_dict[x][1])

    return df


# Work through all games
def dataframes_work(pos_db):

    # Gather list of game IDs
    game_ids = pos_db.collection_names()

    # Loop through game IDs and do stuff
    for game_id in game_ids:

        # Gather an entire game's worth of position data from MongoDB
        pos_coll = pos_db[game_id]

        # Get vital stats
        game_date = pos_coll.find_one()['game_date']
        game_id = pos_coll.find_one()['game_id']

        # Make a list of event IDs
        event_ids = pos_coll.distinct('eventId')

        # Get a single event
        for event_id in event_ids:
            cursor = pos_coll.find({'eventId': event_id})

            # Turn the event into a Pandas dataframe
            for event in cursor:
                pos_df = event_to_df(event, event_id, game_date, game_id)

                # TODO: anything, once we've loaded the event as a dataframe


##########################################################################
## Execution
##########################################################################


# Connect to MongoDB and initialize database 'NBA'
client = MongoClient()
nba_db = client['NBA']
pbp_db = client['PBP']


##########################################################################
## Scratch
##########################################################################


# The following is scratch code used in development. It is not used in the actual execution.


# PrettyPrint syntax
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(document)

