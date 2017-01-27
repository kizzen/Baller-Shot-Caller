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

from sklearn import metrics
from sklearn.cluster import KMeans



##############################
# Import Dataframe and Explore
##############################

# We have an existing pickle.pickle, which is a dataframe of our cleaned SportsVU elements


#dir = os.path.dirname(__file__) #dirname'
os.chdir('/Users/johnniefields/nba-tracking2/nba-tracking/')
filename = os.path.join(os.getcwd(), 'data','pickle.pickle')
filename = 'pickle.pickle'
df= pd.read_pickle(filename)
df.columns

##############################
# Prepare Data for Clustering
##############################
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
# Clustering using Kmeans
#==============================================================================
#defining the object that will carry out the kmeans clustering part.
KMeans_object = KMeans(init = 'k-means++', n_clusters = 17, n_init= 10)
#doing the kmeans clustering
KMeans_object.fit(predictors)

#printing the inertia
print('The Inertia is:', KMeans_object.inertia_)

#Calculating the Homogenity score
print('Homogenity Score is:', metrics.homogeneity_score(outcomes, KMeans_object.labels_))
#Calculating the Completeness Score
print('Completeness Score is:', metrics.completeness_score(outcomes, KMeans_object.labels_))

#calculating the V-measure score
print('V-Measure Score is:', metrics.v_measure_score(outcomes, KMeans_object.labels_))

#calculating the adjusted rand score
print('Adjusted Rand Score is:', metrics.adjusted_rand_score(outcomes, KMeans_object.labels_))

#calculating the adjusted mutual information score
print('Adjusted Mututal Info Score is:', metrics.adjusted_mutual_info_score(outcomes, KMeans_object.labels_))

#Calculating the SIlhoutte Score. We are not sampling the dataset to calculate it.
print('Silhoutte Score is:', metrics.silhouette_score(predictors2, KMeans_object.labels_, metric='euclidean'))
