#!/usr/bin/env python3

class Config(object):
    DEBUG = True
    MESSAGE_BROKER = False
    
class Redis(Config):
    MESSAGE_BROKER = False
    BROKER_NAME = 'Redis'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

