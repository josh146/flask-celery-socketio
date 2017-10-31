#!/usr/bin/env python3

class Config(object):
    DEBUG = True
    MESSAGE_BROKER = False
    
class Redis(Config):
    MESSAGE_BROKER = False
    BROKER_NAME = 'Redis'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

class AWSElastiCache(Config):
    MESSAGE_BROKER = True
    BROKER_NAME = 'AWSElastiCache'
    CELERY_BROKER_URL = 'redis://sfuiredis.xdgpw9.0001.use1.cache.amazonaws.com:6379'
    CELERY_RESULT_BACKEND = 'redis://sfuiredis.xdgpw9.0001.use1.cache.amazonaws.com:6379'
