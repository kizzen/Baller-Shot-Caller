# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 04:02:52 2017

@author: Josh
Run from '__main__' to set up:
    - Initial web scraping
    - set up WORM document store.
    
Note: 
    +Must have a working and active MongoDB session.
    +Must have 2100GB of local space (might change in future iterations to pull to another system)

"""
#==============================================================================
# Imports and dependencies
#==============================================================================
import os
import sys

#Below are local dependencies which are needed to handle initial webscraping.
import ingest.ingest0_dlJSON as dlJSON
import ingest.ingest1_mongoDB as mb
import ingest.ingest1_pos_mongoDB as posmb



if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    ##################
    ##Run Get Games.py to download JSON locally)
    dlJSON.download_games(teamname='SAS')
    
    ##################
    ## Load games into mongo from json
    posmb.mongoData()

    ####################################
    ##Run NBA Play-by-play to mongodb.py
        #!Call spinning up an mongoDB cluster within this
        #export to csv directly.
    mb.pbp_toMongo()
    mb.outputMongo()
    

    
    
        
    #################################
    ## Run CSV_to_joined_dataset.py
    
    
    ## 
    
