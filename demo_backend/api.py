# -*- coding: utf-8 -*-

from demo_backend.extensions import socketio
from flask_socketio import emit
from demo_backend.models import db
import rethinkdb as r
from demo_backend.settings import ProdConfig


@socketio.on('my event')
def test_message(message):
    print 'my event'
    emit('my response', 'yyy')


@socketio.on('search county')
def handle_search(county):
    conn = r.connect(ProdConfig.DB_HOST, ProdConfig.DB_PORT)
    cursor = db.table('township_village').pluck(['county', 'township', 'village', 'coordinates']).run(conn)
    for item in cursor:
        emit('search response', item)

    conn.close()
