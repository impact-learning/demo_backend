# -*- coding: utf-8 -*-

from demo_backend.extensions import socketio
from flask_socketio import emit
from demo_backend.models import db
import rethinkdb as r
from demo_backend.settings import ProdConfig
from demo_backend.modeling import grab_data, grab_impact_data
import pandas as pd
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
    test = data.groupby(['year', 'month']).mean().reset_index()
    test['date'] = pd.to_datetime(pd.DataFrame({
        'year': test.year,
        'month': test.month,
        'day': 1}))
    result = test[['date', 'Score']].to_json(orient='records', date_format='iso')
    emit('response historical data', result)
