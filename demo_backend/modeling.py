import tensorflow as tf
import rethinkdb as r
import numpy as np
import pandas as pd
from demo_backend.models import db
from demo_backend.settings import ProdConfig
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation, metrics, preprocessing
from tensorflow.contrib import learn


def grab_data():
    conn = r.connect('localhost', '28015')
    cursor = db.table('learning').pluck([
            'Score',
            'acu_donation',
            'acu_planting_area',
            'acu_plants',
            'date',
            'month',
            'year',
            'avg_income', 'project_stage']).run(conn)
    villages = []
    for item in cursor:
        villages.append(item)
    conn.close()
    return pd.DataFrame(villages)


def grab_impact_data():
    conn = r.connect('localhost', '28015')
    score_tb = db.table('learning').pluck([
            'Score',
            'acu_donation',
            'acu_planting_area',
            'acu_plants',
            'date',
            'month',
            'year',
            'township_village',
            'average_income-5k',
            'average_income-5k_10k',
            'average_income-10k_15k',
            'average_income-15k_20k',
            'average_income-20k_25k',
            'average_income-25k',
            'avg_income', 'project_stage'])
    coordinates_tb = db.table('township_village_coordinates')
    cursor = score_tb.inner_join(coordinates_tb, lambda s, c: s['township_village'] == c['id']).zip().run(conn)
    villages = []
    for item in cursor:
        villages.append(item)
    conn.close()
    return pd.DataFrame(villages)


def train_model():
    data = grab_data()
    # Pick features for taining
    feature_cols = [col for col in data.columns if col not in [
            u'date',
            u'Score',
            u'coordinates',
            u'id'
        ]]
    x = data[feature_cols].to_dict(orient='records')

    vec = DictVectorizer()
    features = vec.fit_transform(x)

    x = features.toarray()
    y = data[u'Score'].values

    # Split dataset into train / test
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2, random_state=42)

    # Scale data (training set) to 0 mean and unit standard deviation.
    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)

    # Build 2 layer fully connected DNN with 10, 10 units respectively.
    regressor = learn.DNNRegressor(hidden_units=[features.shape[1], round(features.shape[1]/2)])

    # Fit
    regressor.fit(x_train, y_train, steps=5000, batch_size=1)

    # Predict and score
    y_predicted = regressor.predict(scaler.transform(x_test))
    score = metrics.mean_squared_error(y_test, y_predicted)

    print('MSE: {0:f}'.format(score))
    return regressor
