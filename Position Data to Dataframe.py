#!/usr/bin/env python

# Script to convert game event ID stored in MongoDB to Pandas dataframe for analysis

# TODO: Visualize each event as an image, potentially?

# Start MongoDB with custom dbpath
# sudo mongod --dbpath /media/kurt/sd/MongoDB/db

##########################################################################
## Imports
##########################################################################

import json
import pprint
import pandas as pd
import numpy as np
from pymongo import MongoClient
import os

##########################################################################
## Module Variables/Constants
##########################################################################

client = MongoClient()
nba_db = client['NBA']
pbp_db = client['PBP']
os.chdir("C:\\Users\\577731\\Desktop\\nba-tracking\\")

##########################################################################
## Functions
##########################################################################


def printJSON(your_json):
    print(json.dumps(your_json, indent=4, sort_keys=True))


# Print database names and collections
def describe_databases(client):
    d = dict((db, [collection for collection in client[db].collection_names()])
             for db in client.database_names())
    print(json.dumps(d))


# Transform a JSON event into a Pandas dataframe
def event_to_df(event):

    home = event['home']
    visitor = event['visitor']
    moments = event['moments']

    # Column labels
    headers = ["team_id", "player_id", "x_loc", "y_loc", "radius", "moment",
               "game_clock", "shot_clock"]

    # Initialize our new list
    player_moments = []

    for moment in moments:
        # For each player/ball in the list found within each moment
        for player in moment[5]:
            # Add additional information to each player/ball
            # This info includes the index of each moment, the game clock
            # and shot clock values for each moment
            player.extend((moments.index(moment), moment[2], moment[3]))
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
    df["player_jersey"] = df.player_id.map(lambda x: id_dict[x][1])

    return df
	
#return only SAS game_IDs and SAS shots 
def pbp_SAS_dataframe(pbp_CSV_path, game_id):
	pbp_df = pd.DataFrame.from_csv(pbp_CSV_path, header = 1)
	
	# eventsMSGtype defines shots subset only byu these shots.
	pbp_df = pbp_df[ ((pbp_df.EVENTMSGTYPE==2]) | (pbp_df.EVENTMSGTYPE==1])) & (pbp_df.PLAYER1_TEAM_ABBREVIATION=='SAS')&((pbp_df.GAME_ID==game_id))]
	
	df1 = pbp_df['GAME_ID','EVENT_NUM']
	
	uniqueevents = np.array(df1.GAME_ID.unique()).tolist()
	
	return uniqueevents

	
	
# Work through all games
def dataframes_work(nba_db):

    # Gather list of game IDs
    game_ids = nba_db.collection_names()
	
    # Loop through game IDs and do stuff
    for game_id in game_ids:

        coll = nba_db[game_id]

        # Get vital stats
        game_date = coll.find_one()['game_date']
        game_id = coll.find_one()['game_id']
		
        # Make a list of event IDs
        # event_ids = coll.distinct('eventId')
		event_ids = pbp_SAS_dataframe(pbp_CSV_path, game_id)
		
        # Get a single event
        for event_id in event_ids:
            cursor = coll.find({'eventId': event_id})

            # Turn the event into a Pandas dataframe
            for event in cursor:
                df = event_to_df(event)

                # TODO: anything, once we've loaded the event as a dataframe


# TODO: Functions below here don't work.


def travel_dist(player_locations):
    """
    Returns the distance traveled by a player based on his locations
    Parameters
    ----------
    player_locations : pandas DataFrame
        This should be a pandas DataFrame containing 2 columns.  One column
        should contain the x-axis location values and the other column
        should contain the y-axis location values of a player.
    """
    # SO link:
    # https://stackoverflow.com/questions/13590484/
    #   calculating-euclidean-distance-between-consecutive-points-of-an-array-with-numpy
    # get differences of each column
    diff = np.diff(player_locations, axis=0)
    # square the differences and add them,
    # then get the square root of that sum
    dist = np.sqrt((diff ** 2).sum(axis=1))
    # Then return the sum of all the distances
    return dist.sum()


def player_dist(player_a, player_b):
    """
    Returns the distance between two players for each moment they are on the
    court.
    Parameters:
    player_a : pandas DataFrame
        This should be a pandas DataFrame containing 2 columns.  One column
        should contain the x-axis location values and the other column
        should contain the y-axis location values of a player.
    player_b : pandas DataFrame
        This should be a pandas DataFrame containing 2 columns.  One column
        should contain the x-axis location values and the other column
        should contain the y-axis location values of a player.
    ----------
    """
    return [euclidean(player_a.iloc[i], player_b.iloc[i])
            for i in range(len(player_a))]


def draw_court(ax=None, color="gray", lw=1, zorder=0):
    """
    Returns a matplotlib Axes object containing a basketball court
    Parameters
    ----------
    ax : matplotlib Axes
        The matplotlib Axes to plot the basketball court on.  If no Axes is
        provided get the current Axes.
    color : str
        The color of the court lines.
    lw : int
        The lineweight of the court lines.
    zorder : int
        The Z-order of the basketball court.
    """

    if ax is None:
        ax = plt.gca()

    # Creates the out of bounds lines around the court
    outer = Rectangle((0, -50), width=94, height=50, color=color,
                      zorder=zorder, fill=False, lw=lw)

    # The left and right basketball hoops
    l_hoop = Circle((5.35, -25), radius=.75, lw=lw, fill=False,
                    color=color, zorder=zorder)
    r_hoop = Circle((88.65, -25), radius=.75, lw=lw, fill=False,
                    color=color, zorder=zorder)

    # Left and right backboards
    l_backboard = Rectangle((4, -28), 0, 6, lw=lw, color=color,
                            zorder=zorder)
    r_backboard = Rectangle((90, -28), 0, 6, lw=lw, color=color,
                            zorder=zorder)

    # Left and right paint areas
    l_outer_box = Rectangle((0, -33), 19, 16, lw=lw, fill=False,
                            color=color, zorder=zorder)
    l_inner_box = Rectangle((0, -31), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)
    r_outer_box = Rectangle((75, -33), 19, 16, lw=lw, fill=False,
                            color=color, zorder=zorder)

    r_inner_box = Rectangle((75, -31), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)

    # Left and right free throw circles
    l_free_throw = Circle((19, -25), radius=6, lw=lw, fill=False,
                          color=color, zorder=zorder)
    r_free_throw = Circle((75, -25), radius=6, lw=lw, fill=False,
                          color=color, zorder=zorder)

    # Left and right corner 3-PT lines
    # a represents the top lines
    # b represents the bottom lines
    l_corner_a = Rectangle((0, -3), 14, 0, lw=lw, color=color, zorder=zorder)
    l_corner_b = Rectangle((0, -47), 14, 0, lw=lw, color=color, zorder=zorder)
    r_corner_a = Rectangle((80, -3), 14, 0, lw=lw, color=color, zorder=zorder)
    r_corner_b = Rectangle((80, -47), 14, 0, lw=lw, color=color, zorder=zorder)

    # Left and right 3-PT line arcs
    l_arc = Arc((5, -25), 47.5, 47.5, theta1=292, theta2=68, lw=lw,
                color=color, zorder=zorder)
    r_arc = Arc((89, -25), 47.5, 47.5, theta1=112, theta2=248, lw=lw,
                color=color, zorder=zorder)

    # half_court
    # ax.axvline(470)
    half_court = Rectangle((47, -50), 0, 50, lw=lw, color=color, zorder=zorder)

    hc_big_circle = Circle((47, -25), radius=6, lw=lw, fill=False,
                           color=color, zorder=zorder)
    hc_sm_circle = Circle((47, -25), radius=2, lw=lw, fill=False,
                          color=color, zorder=zorder)

    court_elements = [l_hoop, l_backboard, l_outer_box, outer,
                      l_inner_box, l_free_throw, l_corner_a,
                      l_corner_b, l_arc, r_hoop, r_backboard,
                      r_outer_box, r_inner_box, r_free_throw,
                      r_corner_a, r_corner_b, r_arc, half_court,
                      hc_big_circle, hc_sm_circle]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax



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

