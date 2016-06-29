# -*- coding: utf-8 -*-

from demo_backend.extensions import socketio
from flask_socketio import emit
from demo_backend.models import db
import rethinkdb as r
from demo_backend.settings import ProdConfig
from demo_backend.modeling import preprocessing_data


@socketio.on('my event')
def test_message(message):
    print 'my event'
    emit('my response', 'yyy')


@socketio.on('search county')
def handle_search(county):
    conn = r.connect(ProdConfig.DB_HOST, ProdConfig.DB_PORT)
    cursor = db.table('township_village').pluck(['county', 'township', 'village', 'coordinates', 'scores', 'average_income_per_capita', 'number_of_trees']).run(conn)
    villages = []
    for item in cursor:
        villages.append(item)
    emit('search response', villages)

    conn.close()
    print 'Handle Serach'
