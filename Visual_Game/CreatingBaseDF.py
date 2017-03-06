import numpy as np
import pickle
import os

# 3rd party
import pandas as pd
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
os.chdir('/Users/khalilezzine/Desktop/DS/')
filename = os.path.join(os.getcwd(), 'Visual_Game','pickle.pickle')
#
df= pd.read_pickle(filename)
# df.columns
# df = pd.read_csv('/Users/khalilezzine/Desktop/LOOKatPickle.csv')
# print (type(df))
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
# SVM Model Fitting parameters
#==============================================================================
# print("Fitting the classifier to the training set")
# t0 = time()
# param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
#               'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
# gs_clf = GridSearchCV(svm.SVC(kernel='rbf', class_weight='balanced'), param_grid)
# gs_clf.fit(predictors, outcomes)
# gs_svm_predicted = clf.predict(predictors)
#
#
# clf = svm.SVC(kernel='rbf', class_weight='balanced')
# clf.fit(predictors, outcomes)
#
# svm_predicted = clf.predict(predictors)
# accuracy_score(outcomes, svm_predicted)
#
#
# print("done in %0.3fs" % (time() - t0))
# print("Best estimator found by grid search:")
# print(clf.best_estimator_)




#==============================================================================
# RandomForest (Classifier Variant) Model Fitting parameters
#==============================================================================

estimator = Pipeline([("forest", RandomForestClassifier(random_state=0, n_estimators=100))])
estimator.fit(predictors, outcomes)

predicted = estimator.predict(predictors)
prediction_scores  = accuracy_score(outcomes, predicted) #This code will change, fi we cross validate

# print (type(predicted[2]))
# print (predicted[2])
lst_predicted = []
for i in predicted:
    if i == 202695:
        lst_predicted.append('Kawhi Leonard')
    elif i == 1495:
        lst_predicted.append('Tim Duncan')
    elif i == 2225:
        lst_predicted.append('Tony Parker')
    elif i == 200746:
        lst_predicted.append('LaMarcus Aldridge')
    elif i == 1938:
        lst_predicted.append('Manu Ginobili')
    elif i == 2446:
        lst_predicted.append('Rasual Butler')
    elif i == 2564:
        lst_predicted.append('Boris Diaw')
    elif i == 201980:
        lst_predicted.append('Danny Green')
    elif i == 2561:
        lst_predicted.append('David West')
    elif i == 203937:
        lst_predicted.append('Kyle Anderson')
    elif i == 201988:
        lst_predicted.append('Patty Mills')
    elif i == 1626246:
        lst_predicted.append('Boban Marjanovic')
    elif i == 203492:
        lst_predicted.append('Ray McCallum')
    elif i == 203613:
        lst_predicted.append('Jonathon Simmons')
    else:
        lst_predicted.append('Matt Bonner')

df_predicted = pd.DataFrame(lst_predicted)
df_predicted.columns = ['Predicted']
# print (type(df_predicted))
# df_predicted.to_csv('/Users/khalilezzine/Desktop/what.csv')
# print (df_predicted.shape)
df_readywr = pd.concat([df_predicted, df], axis=1)
df_readywr.to_csv('/Users/khalilezzine/Desktop/df_w_predicted.csv')

# for i in lst_predicted:
#         if i == 'Kawhi Leonard':
#             lst_predicted.append(0)
#         elif i == 'Tim Duncan':
#             lst_predicted.append(0)
#         elif i == 'Tony Parker':
#             lst_predicted.append(0)
#         elif i == 'LaMarcus Aldridge':
#             lst_predicted.append(0)
#         elif i == 'Manu Ginobili':
#             lst_predicted.append(0)
#         elif i == 'Rasual Butler':
#             lst_predicted.append(0)
#         elif i == 'Boris Diaw':
#             lst_predicted.append(0)
#         elif i == 'Danny Green':
#             lst_predicted.append(0)
#         elif i == 'David West':
#             lst_predicted.append(0)
#         elif i == 'Kyle Anderson':
#             lst_predicted.append(0)
#         elif i == 'Patty Mills':
#             lst_predicted.append(0)
#         elif i == 'Boban Marjanovic':
#             lst_predicted.append(0)
#         elif i == 'Ray McCallum':
#             lst_predicted.append(0)
#         elif i == 'Jonathon Simmons':
#             lst_predicted.append(0)
#         elif i == 'Matt Bonner':
#             lst_predicted.append(0)
#         else:
#             lst_predicted.append(1)
# print (sum(lst_predicted))
#test_predicted = estimator.predict(test_predictors)
#prediction_scores  = accuracy_score(test_outcomes, test_predicted)
#
# with open(os.path.join(os.getcwd(), 'data','RF.pickle'), 'wb') as pickle_file:
#     pickle.dump(estimator, pickle_file)
#
# max(predictors[0])
#
#
#
# print("Score after imputation of the missing values = %.2f" % score)
