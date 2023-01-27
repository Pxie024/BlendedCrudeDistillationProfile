import pandas as pd
import numpy as np 

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.naive_bayes import MultinomialNB 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.impute import SimpleImputer 
from sklearn.metrics import make_scorer, r2_score, mean_squared_error, auc, mean_absolute_error, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator


import matplotlib.pyplot as plt
import seaborn as sns


from DataCleaner import CleanData 
import random
import numbers



# the function to calculate mixing rules 
def mix_crude(oil_1, vol_1, oil_2, vol_2, feature_df):
    """
    For all properties, the mixed results will be (p1*v1 + p2*v2) / (v1+v2),
    where p1, and p2 are the corresponding property values for oil 1 and oil 2.
    """
    assert isinstance(vol_1, numbers.Number)
    assert isinstance(vol_2, numbers.Number) 
    
    property_1 = feature_df.loc[oil_1]
    property_2 = feature_df.loc[oil_2]
    
    property_mix = (property_1*vol_1 + property_2*vol_2) / (vol_1 + vol_2)
    return property_mix.T



# build a model switcher to try different regression models in using the pipeline
class modelSwitcher(BaseEstimator):
    
    def __init__(self, estimator=Lasso()):
        """
        A Custom BaseEstimator that can switch between regression models.

        Parameters:
        ----------
        estimator: sklearn object - The regression model. Can take values in 
        [Lasso(), RandomForestRegressor(), KNeighborsRegressor(), LinearRegression()]
        """ 

        self.estimator = estimator
    
    
    def fit(self, X, y=None, **kwargs):
        self.estimator.fit(X, y)
        return self


    def predict(self, X, y=None):
        return self.estimator.predict(X)


    def score(self, X, y):
        return self.estimator.score(X, y)



# Building pipeline 
estimators = [('scaler', StandardScaler()), ('reduce_dim', PCA()), ('model', modelSwitcher())]
pipe = Pipeline(estimators)

parameters = [{
        'model__estimator': [Lasso()], 
        'reduce_dim__n_components': [2,5,10,20],
        'model__estimator__alpha': [1.0, 5.0, 10.0, 20.0],
        'model__estimator__fit_intercept': [True, False]
    }, 
    {
        'model__estimator': [RandomForestRegressor()],
        'reduce_dim__n_components': [2,5,10,20],
        'model__estimator__n_estimators': [5, 20, 50, 100, 200],
        'model__estimator__max_depth': [3, 5, 10, 20, None],
        'model__estimator__max_features' : ["auto", "sqrt", "log2"]
    },
    {
        'model__estimator': [KNeighborsRegressor()],
        'reduce_dim__n_components': [2,5,10,20],
        'model__estimator__n_neighbors': [2, 5, 8, 10, 20],
        'model__estimator__weights': ['uniform', 'distance']
    },
    {
        'model__estimator': [LinearRegression()],
        'reduce_dim__n_components': [2,5,10,20],
        'model__estimator__fit_intercept': [True, False]
    }
]

Model = GridSearchCV(pipe, param_grid=parameters, cv=5, n_jobs=12)