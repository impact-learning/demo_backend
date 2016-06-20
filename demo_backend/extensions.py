# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO

debug_toolbar = DebugToolbarExtension()
socketio = SocketIO()
