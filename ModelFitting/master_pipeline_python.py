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

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


##############################
# Data munging support functions and initial import of files
##############################

# We have an existing pickle.pickle, which is a dataframe of our cleaned SportsVU elements
 #dir = os.path.dirname(__file__) #dirname'
os.chdir('C:\\Users\\Josh\\Documents\\nba-tracking\\')
filename = os.path.join(os.getcwd(), 'data','pickle.pickle')

df= pd.read_pickle(filename)
crosswalk = pd.read_csv("./data/gameIDcrosswalk.csv")

#df.columns
#df.shape
#df.view()

#player id is the person who took the shot, as file has already been subset to only shot taking events.


#need to identify tuples for our columns.
def gen_predictors_outcomes(df):
    colnames_pred = []
    for i in df.columns:
        if isinstance(i, tuple):
            colnames_pred.append(i)
    colnames_pred = colnames_pred[2:]
            
    len(colnames_pred)
    
    ####Imputing values for players in bench
    predictors = df[colnames_pred]
    predictors.fillna(-200, inplace = True)
    outcomes = df['PLAYER1_NAME']
    outcomes = outcomes.astype('category') #Make sure the integers are represented as categorical data
    #Code for encoding position on the court. Might not be necessary.
    #for i in range(0,15):
    #    x = i * 30
    #    predictorsFinal[SpursList[i]] = np.where(predictors2.iloc[:,x]==-200, 0, 1)
    
    predictors2 = predictors[np.isfinite((predictors.values)).any(axis=1)]
    outcomes2 = outcomes[np.isfinite((predictors.values)).any(axis=1)]
        
    #eliminated -100 predictors until later step.
    return predictors2, outcomes2
    
predictors, outcomes = gen_predictors_outcomes(df)
    
def halftime_xlist(predict_trans):
    holdingcol = []
    for (xvar, obs, name) in predict_trans.columns.values:
        if xvar == 'x_loc':
            tupler = (xvar, obs, name)
            holdingcol.append(tupler)
    return holdingcol
    
#Makes all left values inverted. Could probably combine these into one column with and if then statemetn.
def halftime_ylist(predict_trans):
    holdingcol = []
    for (xvar, obs, name) in predict_trans.columns.values:
        if xvar == 'y_loc':
            tupler = (xvar, obs, name)
            holdingcol.append(tupler)
    return holdingcol

def halftime_transform(prediction_df):
    predict_trans = prediction_df
    column_listx = halftime_xlist(predict_trans)
    column_listy = halftime_ylist(predict_trans)
    
    predict_trans['CourtCount'] = 0 
    #Counter of how many x coordinates are on the left side of the court vs the right.

    for i in column_listx:
        predict_trans['CourtCount'] = np.where(predict_trans[i] >= 47, predict_trans['CourtCount']+1, predict_trans['CourtCount'])
        predict_trans['CourtCount'] = np.where(predict_trans[i] <  47, predict_trans['CourtCount']-1, predict_trans['CourtCount'])
        #Double check NA handling.
    
    
    for i in column_listx:
        predict_trans[i] = np.where(predict_trans['CourtCount'] < -5, 95-predict_trans[i], predict_trans[i])

    for i in column_listy:
        predict_trans[i] = np.where(predict_trans['CourtCount'] < -5, 50-predict_trans[i], predict_trans[i])

        
    predict_trans.fillna(-200, inplace = True)
    predict_trans = predict_trans.ix[:,0:900]#We can finally fill in our NA's once we've fixed our shit.
    return predict_trans
    
predictors = halftime_transform(predictors)








##Generate Training Set and Testing Set
# predictorsFinal[pd.isnull(predicto).any(axis=1)]
############Gross Fitting: Primaries only.
#==============================================================================
# Modelling class (Classifier Variant) Model Fitting parameters
#==============================================================================

class MultModels:
    def __init__(self, df):
        self.predictors, self.outcomes = gen_predictors_outcomes(df)
      
    def rf(self):
        self.estimator = Pipeline([("forest", RandomForestClassifier(random_state=0, n_estimators=50))])
        #add type
        self.scor_vis()
        
    def adaboost(self):
        self.estimator = Pipeline([("AdaBoost", AdaBoostClassifier())])
        self.scor_vis()
                
    def svm(self):
        #train_test_split
        clf = svm.SVC(kernel='rbf', class_weight='balanced')
        clf.fit(self.predictors, self.outcomes)
        svm_predicted = clf.predict(predictors)
        accuracy_score(outcomes, svm_predicted)
                
    def scor_vis(self): #Need to add specifics and means.
        accuracy = np.mean(cross_val_score(self.estimator, self.predictors, self.outcomes, cv=8))
        precision = np.mean(cross_val_score(self.estimator, self.predictors, self.outcomes, cv=8))
        recall = np.mean(cross_val_score(self.estimator, self.predictors, self.outcomes, cv=8)) 
        f1 = np.mean(cross_val_score(self.estimator, self.predictors, self.outcomes, cv=8)) 
#test_predicted = estimator.predict(test_predictors) 
#prediction_scores  = accuracy_score(test_outcomes, test_predicted)
        print("accuracy: {}".format(accuracy))
        print("precision: {}".format(precision))
        print("recall: {}".format(recall))
        print("f1: {}".format(f1))

if __name__ == "__main__":
    nbaModels = MultModels(df)
    nbaModels.rf()
 


