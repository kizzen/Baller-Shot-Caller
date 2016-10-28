# -*- coding: utf-8 -*-
import json
import pymongo
from pprint import pprint
import csv
import glob
import os
import sys
#%%#######################################################################
## establishing mongo connection, only after you get mongod.exe is running 
# C:\Program Files\MongoDB\Server\3.2\bin
##########################################################################
conn=pymongo.MongoClient()
db = conn.mydb
conn.database_names()
collection = db.PbP_Full


#%%#######################################################################
## Import of JSONS into mongo; not necessary to run if you already have my mongo database itself
##########################################################################


if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]))
    list_jsons = glob.glob('.\\data\\PlaybyPlay\\*.json') 

for x in list_jsons:
    data_file=x
    with open(data_file) as data_file:    
        singleLoad = json.load(data_file)
    singlePbP = singleLoad['_playbyplay']['resultSets']['PlayByPlay']
    for i in singlePbP:
        collection.insert_one(i)
    
#pprint to identify where the game events are actually present.


#%%#######################################################################
## Outputting to CSV directly from mongo. Pretty sleek yo.
##########################################################################

cursor = collection.find({"$or":[ {"PLAYER1_TEAM_ABBREVIATION":"SAS"}, {"PLAYER2_TEAM_ABBREVIATION":"SAS"}, {"PLAYER3_TEAM_ABBREVIATION":"SAS"}]})
def pbp_csv_to_mongo(cursor):
    with open('pbp_SAS.csv', 'a', newline='') as outfile:
        fields = ['SCORE', 'PERSON3TYPE', 'PLAYER3_NAME', 'PLAYER3_TEAM_CITY', 'VISITORDESCRIPTION', 'PLAYER1_ID', 'PERSON1TYPE', 'PERIOD', 'PLAYER1_TEAM_NICKNAME', 'HOMEDESCRIPTION', 'PLAYER1_TEAM_ID', '_id', 'WCTIMESTRING', 'PLAYER2_TEAM_NICKNAME', 'SCOREMARGIN', 'PLAYER2_NAME', 'PCTIMESTRING', 'PLAYER3_TEAM_NICKNAME', 'PLAYER1_TEAM_CITY', 'PLAYER2_ID', 'EVENTMSGTYPE', 'GAME_ID', 'PERSON2TYPE', 'EVENTNUM', 'PLAYER1_NAME', 'PLAYER3_ID', 'PLAYER3_TEAM_ABBREVIATION', 'PLAYER2_TEAM_ABBREVIATION', 'EVENTMSGACTIONTYPE', 'PLAYER3_TEAM_ID', 'PLAYER2_TEAM_CITY', 'NEUTRALDESCRIPTION', 'PLAYER2_TEAM_ID', 'PLAYER1_TEAM_ABBREVIATION']
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)
        
def array_front9(nums):
  count = 0
  for i in range(0,3):
    count = count + 1
  return  count