"""
======================================================
Imputing missing values before building an estimator
======================================================

This example shows that imputing the missing values can give better results
than discarding the samples containing any missing value.
Imputing does not always improve the predictions, so please check via cross-validation.
Sometimes dropping rows or using marker values is more effective.

Missing values can be replaced by the mean, the median or the most frequent
value using the ``strategy`` hyper-parameter.
The median is a more robust estimator for data with high magnitude variables
which could dominate results (otherwise known as a 'long tail').

Script output::

  Score with the entire dataset = 0.56
  Score without the samples containing missing values = 0.48
  Score after imputation of the missing values = 0.55

In this case, imputing helps the classifier get close to the original score.
  
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
colnames_pred = []
for i in df.columns:
    if isinstance(i, tuple):
        colnames_pred.append(i)
colnames_pred = colnames_pred[2:]
        
len(colnames_pred)

####Imputing values for players in bench
predictors = df[colnames_pred]
type(predictors)

for i in predictors:
    predictors[i].fillna(-100, inplace= True)

type(predictors)
    
#==============================================================================
# Model fitting part 2?
#==============================================================================

#==============================================================================
# # fit the model
# clf = svm.NuSVC()
# clf.fit(predictors, outcomes)
# 
# # plot the decision function for each datapoint on the grid
# Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
# Z = Z.reshape(xx.shape)
# 
# plt.imshow(Z, interpolation='nearest',
#            extent=(xx.min(), xx.max(), yy.min(), yy.max()), aspect='auto',
#            origin='lower', cmap=plt.cm.PuOr_r)
# contours = plt.contour(xx, yy, Z, levels=[0], linewidths=2,
#                        linetypes='--')
# plt.scatter(X[:, 0], X[:, 1], s=30, c=Y, cmap=plt.cm.Paired)
# plt.xticks(())
# plt.yticks(())
# plt.axis([-3, 3, -3, 3])
# plt.show()
#==============================================================================
    
    
#==============================================================================
# Model Fitting parameters
#==============================================================================
print("Fitting the classifier to the training set")
t0 = time()
param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
clf = clf.fit(X_train_pca, y_train)
print("done in %0.3fs" % (time() - t0))
print("Best estimator found by grid search:")
print(clf.best_estimator_)




estimator = Pipeline([("forest", RandomForestClassifier(random_state=0, n_estimators=100))])
estimator.fit(predictors, outcomes)

predicted = estimator.predict(predictors) 
prediction_scores  = accuracy_score(outcomes, predicted) #This code will change, fi we cross validate

#test_predicted = estimator.predict(test_predictors) 
#prediction_scores  = accuracy_score(test_outcomes, test_predicted)

with open(os.path.join(os.getcwd(), 'data','RF.pickle'), 'wb') as pickle_file:
    pickle.dump(estimator, pickle_file)

max(predictors[0])



print("Score after imputation of the missing values = %.2f" % score)



