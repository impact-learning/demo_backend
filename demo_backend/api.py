# -*- coding: utf-8 -*-

from demo_backend.extensions import socketio
from flask_socketio import emit
from flask import session


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})
