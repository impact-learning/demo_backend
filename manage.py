#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Management Script
"""

import os

from flask_script import Manager
from flask_script.commands import ShowUrls, Clean
from demo_backend import create_app
from demo_backend.extensions import socketio
from demo_backend.models import db_setup, db
from tornado.ioloop import IOLoop


# default to dev config because no one should use this in
# production anyway
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

env = os.environ.get('DEMO_BACKEND_ENV', 'dev')
app = create_app('demo_backend.settings.%sConfig' % env.capitalize())


manager = Manager(app)


@manager.command
def runserver():
    """ run the server for dev
    """
    # db_setup()  # Check DB and Tables were pre created
    socketio.run(app, debug=True)

    IOLoop.instance().start()


@manager.shell
def make_shell_context():
    """ Make Shell Context

    Creates a python REPL with several default imports in the context of the app.
    """
    return dict(app=app, db=db)


# @manager.command
# def init_data():
#     """Initialize database"""
#     db_setup()


# manager.add_command("init_db", init_data())
manager.add_command('server', runserver())
manager.add_command('shell', make_shell_context())
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())


if __name__ == "__main__":
    manager.run()
