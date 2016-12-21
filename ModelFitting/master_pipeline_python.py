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
    
    predictors.fillna(-100, inplace= True)
        
    return predictors
    
predictors = gen_predictors(df)
df.max()
df.min()
type(predictors)

    
#==============================================================================
# RandomForest (Classifier Variant) Model Fitting parameters
#==============================================================================

estimator = Pipeline([("forest", RandomForestClassifier(random_state=0, n_estimators=100))])
estimator.fit(predictors, outcomes)

predicted = estimator.predict(predictors) 
prediction_scores  = accuracy_score(outcomes, predicted) #This code will change, fi we cross validate

#test_predicted = estimator.predict(test_predictors) 
#prediction_scores  = accuracy_score(test_outcomes, test_predicted)

print(prediction_scores)

with open(os.path.join(os.getcwd(), 'data','RF.pickle'), 'wb') as pickle_file:
    pickle.dump(estimator, pickle_file)






