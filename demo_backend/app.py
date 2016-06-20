# -*- coding: utf-8 -*-
"""
    The app module, containing the app factory function.
"""

from flask import Flask
from demo_backend.settings import ProdConfig
from demo_backend.extensions import debug_toolbar, socketio


def create_app(object_name=ProdConfig):
    """ An flask application factory

    as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. demo_backend.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """
    app = Flask(__name__)
    app.config.from_object(object_name)

    register_extensions(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    debug_toolbar.init_app(app)
    socketio.init_app(app)
    return None
