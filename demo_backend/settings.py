# -*- coding: utf-8 -*-
class Config(object):
    SECRET_KEY = 'secret key'
    DB_NAME = 'impact_learning'


class ProdConfig(Config):
    ENV = 'prod'
    DB_HOST = 'localhost'
    DB_PORT = '28015'

    CACHE_TYPE = 'simple'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    DB_HOST = 'localhost'
    DB_PORT = '28015'

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    DB_HOST = 'localhost'
    DB_PORT = '28015'

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
