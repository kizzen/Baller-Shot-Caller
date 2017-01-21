"""

In this case, imputing helps the classifier get close to the original score.

Cross Validation Link:
http://scikit-learn.org/stable/auto_examples/model_selection/grid_search_digits.html#sphx-glr-auto-examples-model-selection-grid-search-digits-py
  
"""

##############################
# Module imports and dependencies
##############################

import numpy as np
import pandas as pd
import pickle
import os
import sklearn

from sklearn.metrics import accuracy_score
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


##############################
# Import Dataframe and Explore
##############################

# We have an existing pickle.pickle, which is a dataframe of our cleaned SportsVU elements
 

#dir = os.path.dirname(__file__) #dirname'
os.chdir('C:\\Users\\Josh\\Documents\\nba-tracking\\')
filename = os.path.join(os.getcwd(), 'data','pickle.pickle')

df= pd.read_pickle(filename)
df.columns


#player id is the person who took the shot, as file has already been subset to only shot taking events.
testlist = ['PLAYER1_ID', 'PERSON3TYPE']
broketest = df[testlist]

outcomes = df['PLAYER1_ID']
outcomes = outcomes.astype('category')


#need to identify tuples for our columns.
def gen_predictors(df):
    colnames_pred = []
    for i in df.columns:
        if isinstance(i, tuple):
            colnames_pred.append(i)
    colnames_pred = colnames_pred[2:]
            
    len(colnames_pred)
    
    ####Imputing values for players in bench
    predictors = df[colnames_pred]
    type(predictors)
    #eliminated -100 predictors until later step.
        
    return predictors
    
pred_trans = gen_predictors(df)
pred_trans.ix[:,1].describe() #Identify xmax range, 100
pred_trans.ix[:,899].describe() #identify ymax range, 50
 #identify ymin, 0


#==============================================================================
# Transform predictors so that our 
#==============================================================================

## How to only iterate over the tuples of a list???

#Fix the -100s..... for x coordinates.
#get all column names with 'xloc'
def halftime_xlist(predict_trans):
    holdingcol = []
    for (xvar, obs, name) in predict_trans.columns.values:
        if xvar == 'x_loc':
            tupler = (xvar, obs, name)
            holdingcol.append(tupler)
    return holdingcol
    
#Makes all left values inverted. Could probably combine these into one column with and if then statemetn.
def halftime_ylist(predictors):
    holdingcol = []
    for (xvar, obs, name) in predictors.columns.values:
        if xvar == 'y_loc':
            tupler = (xvar, obs, name)
            holdingcol.append(tupler)
    return holdingcol
    

#only works if all numpy operations are vectorized...don't have to specify observation number.
#Can simply say, if column a, then column b does this, for all observations within each column.

def halftime_transform(prediction_df):
    predict_trans = prediction_df
    column_listx = halftime_xlist(predict_trans)
    column_listy = halftime_ylist(predict_trans)
    
    predict_trans['CourtCount'] = 0 
    #Counter of how many x coordinates are on the left side of the court vs the right.

    for i in column_listx:
        predict_trans['CourtCount'] = np.where(predict_trans[i] >= 48, predict_trans['CourtCount']+1, predict_trans['CourtCount'])
        predict_trans['CourtCount'] = np.where(predict_trans[i] <  48, predict_trans['CourtCount']-1, predict_trans['CourtCount'])
        #Double check NA handling.
    
    
    for i in column_listx:
        predict_trans[i] = np.where(predict_trans['CourtCount'] < -5, 95-predict_trans[i], predict_trans[i])

    for i in column_listy:
        predict_trans[i] = np.where(predict_trans['CourtCount'] < -5, 50-predict_trans[i], predict_trans[i])

        
    predict_trans.fillna(-200, inplace = True) #We can finally fill in our NA's once we've fixed our shit.
    return predict_trans


predictors = halftime_transform(pred_trans)
predictors.CourtCount.describe()
len(predictors2.columns)
predictors2 = predictors.ix[:,0:900]
type(predictors)
df[('x_loc', 29, 'Boris Diaw')] # just test code to ensure that this shitzle works.


    
#==============================================================================
# RandomForest (Classifier Variant) Model Fitting parameters
#==============================================================================
  
estimator = Pipeline([("forest", RandomForestClassifier(random_state=0, n_estimators=100))])
estimator.fit(predictors2, outcomes)

predicted = estimator.predict(predictors2) 
prediction_scores  = accuracy_score(outcomes, predicted) #This code will change, fi we cross validate

#test_predicted = estimator.predict(test_predictors) 
#prediction_scores  = accuracy_score(test_outcomes, test_predicted)

print(prediction_scores)

with open(os.path.join(os.getcwd(), 'data','RF.pickle'), 'wb') as pickle_file:
    pickle.dump(estimator, pickle_file)






