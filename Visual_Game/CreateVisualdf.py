# import modules
import csv
import pickle

# 3rd party
import pandas as pd

# make sure to include the correct file path
dfbis = pd.read_csv('/Users/awei/documents/workspace/Baller-Shot-Caller/Visual_Game/df_w_predicted.csv')

#'Predicted' is model prediction, 'PLAYER1_NAME' is who actually took the shot
dfbis1 = dfbis[['Predicted', 'PLAYER1_NAME']]

'''We now create a new dataframe from pickle which includes the x,y coordinates for the
following players: Danny Green, Kawhi Leonard, LaMarcus Aldridge, Tim Duncan and
Tony Parker.'''

ddfbis=pd.read_pickle('/Users/awei/documents/workspace/Baller-Shot-Caller/Data/pickle.pickle')
dfbis2 = ddfbis.iloc[:,35:]#selecting only columns with x,y coordinated

# drop column if it does not contain one the these 5 players
for item in dfbis2.columns:
    if item[2]=="Danny Green":
        pass
    elif item[2]=="Kawhi Leonard":
        pass
    elif item[2]=="LaMarcus Aldridge":
        pass
    elif item[2]=="Tim Duncan":
        pass
    elif item[2]=="Tony Parker":
        pass
    else:
        dfbis2.drop(item, axis=1, inplace=True)

final_dbis = pd.concat([dfbis1,dfbis2],axis=1) #includes the df above with x,y values

final_dbis.dropna(how='any',inplace=True) # drop play if player is on the bench
final_dbis.reset_index(inplace=True)
del final_dbis['index']

final_dbis.to_csv('/Users/awei/documents/workspace/Baller-Shot-Caller/Visual_Game/df4plot1.csv')
