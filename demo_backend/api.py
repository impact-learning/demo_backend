# -*- coding: utf-8 -*-

from demo_backend.extensions import socketio
from flask_socketio import emit
from demo_backend.models import db
import rethinkdb as r
from demo_backend.settings import ProdConfig
from demo_backend.modeling import grab_data, grab_impact_data
import pandas as pd
import numpy as np
import datetime


@socketio.on('my event')
def test_message(message):
    print 'my event'
    emit('my response', 'yyy')


@socketio.on('search county')
def handle_search(county):
    data = grab_impact_data()
    data['date'] = pd.to_datetime(pd.DataFrame({
            'year': data.year,
            'month': data.month,
            'day': 1}))
    result = data.to_json(orient='records', date_format='iso')
    emit('search response', result)


@socketio.on('get historical data')
def handle_historical():
    data = grab_data()
    test = data.groupby(['year', 'month'])['Score'].agg([np.mean, np.median, np.max, np.min, np.var, np.std]).reset_index()
    test.columns = ['year', 'month', 'Score', 'median', 'amax', 'amin', 'var', 'std']
    test['date'] = pd.to_datetime(pd.DataFrame({
        'year': test.year,
        'month': test.month,
        'day': 1}))
    result = test[['date', 'Score', 'median', 'amax', 'amin', 'var', 'std']].to_json(orient='records', date_format='iso')
    emit('response historical data', result)
