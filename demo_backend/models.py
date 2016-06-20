# -*- coding: utf-8 -*-
import rethinkdb as r
# from tornado.concurrent import Future
# import functools
from demo_backend.settings import ProdConfig
from rethinkdb.errors import RqlRuntimeError


db_connection = r.connect(ProdConfig.DB_HOST, ProdConfig.DB_PORT)


def db_setup():
    try:
        r.db_create(ProdConfig.DB_NAME).run(db_connection)
    except RqlRuntimeError:
        print 'Database already exists. Nothing to do.'

    db_connection.close()

r.set_loop_type("tornado")
db = r
