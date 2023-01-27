from flask import Flask, render_template, request
import pandas as pd 
import numpy as np 
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, validators, DecimalField
from DataCleaner import CleanData
from CrudeBlendModel import mix_crude, Model

import random

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


# Load Data 
crude_data = CleanData()
x_data , Y_data = crude_data.get_x_y_data()

# normalize x_data 
random.seed(10)
impX = SimpleImputer(missing_values=np.nan, strategy='mean')
scaler = StandardScaler()
x_data = x_data.apply(lambda row: row.replace(np.nan, row.mean()), axis=1)
Y_data = Y_data.apply(lambda row: row.replace(np.nan, max(row)), axis=1)

all_oils = Y_data.index.values

# fit the data
Model.fit(x_data, Y_data)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

report_pct = [5,10,20,30,40,50,60,70,80,90,95,99]


# class Form(FlaskForm):
#     crude_oil_1 = SelectField('type 1', choices=all_oils)
#     oil_1_vol = DecimalField('type 1 volume', [validators.InputRequired()])
#     crude_oil_2 = SelectField('type 2', choices=all_oils)
#     oil_2_vol = DecimalField('type 2 volume', [validators.InputRequired()])


@app.route('/')
@app.route('/input')
def index():
    return render_template('index.html', 
            data = x_data, all_oils=all_oils)

@app.route('/output', methods=['GET', 'POST'])
def submit():
    # form = Form()
    if request.method == 'POST':
        req = request.form
        oil_1 = req['oil_1_select']
        oil_2 = req['oil_2_select']
        vol_1 = req['oil_1_vol']
        vol_2 = req['oil_2_vol']

        if oil_1 == oil_2:
            predictions = Y_data.loc[oil_1].values
        else:
            mixed_data = mix_crude(oil_1, float(vol_1),
                                oil_2, float(vol_2), x_data)
            predictions = Model.predict([mixed_data])[0]
        
        results = {}
        for i in range(len(predictions)):
            print(predictions)
            results[report_pct[i]] = predictions[i]
        return render_template('output.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)