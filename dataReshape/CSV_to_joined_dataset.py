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
import os
import glob


##########################################################################
## Imports
##########################################################################

mydir = "C:\\Users\\577731\\Desktop\\nba-tracking"
os.chdir(mydir)

#Find list of data frames, and then prune that list.
filenames = glob.glob(mydir + "\\*.csv")

#CSVs are imported into a merged dataframe, 
def csv_to_pruned_dataframe(filenames):
    headers = ["index", "team_id", "player_id", "x_loc", "y_loc", "radius", "moment",
               "game_clock", "shot_clock", "event_id", "game_date", "game_id", "PlayerName"]
    list_ = []
    for filename in filenames:
        df = pd.read_csv(filename,index_col=None, header=0, names=headers)
        #calling our subsample
        sub_df = subsample(df)
        sub_df.pivot(index='patient', columns='obs', values='score')
        list_.append(sub_df)
    frame = pd.concat(list_)
        

##########################################################################
## Execution
##########################################################################        


##########################################################################
## Scrap
##########################################################################        

#Check the number of observations per player, per play
#df[['col1', 'col2', 'col3', 'col4']].groupby(['col1', 'col2']).agg(['mean', 'count'])

# http://stackoverflow.com/questions/11786157/if-list-index-exists-do-x


def subsample(df):
    #drop off other things?
    
    #Creates a Group by object (which includes an index separated into groups that restart once a new group begins, enabling aggregate functions)
    g = df.groupby(['EVENTNUM', 'player_id'])
    
    g = g[g.cumcount()%5==0] #g[] vs df[]? 
    
    #Reduce dimensions.
    g = g.tail(100).reset_index(drop=True)
    
    #Backwards index for pivot?
        g = g.nth(5)
    #need to fi the type of error
    except:
        pass
    

    result = df.sort(['A', 'B'], ascending=[0, 0, 0, 0])
    

### Grab every nth item 10x times (if available)
GroupBy.count() 	Compute count of group, excluding missing values
GroupBy.cumcount([ascending]) 	Number each item in each group from 0 to the length of that group - 1.
GroupBy.first() 	Compute first of group values
GroupBy.head([n]) 	Returns first n rows of each group.
GroupBy.last() 	Compute last of group values
GroupBy.max() 	Compute max of group values
GroupBy.mean(\*args, \*\*kwargs) 	Compute mean of groups, excluding missing values
GroupBy.median() 	Compute median of groups, excluding missing values
GroupBy.min() 	Compute min of group values
GroupBy.nth(n[, dropna]) 	Take the nth row from each group if n is an int, or a subset of rows if n is a list of ints.


