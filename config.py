#!/usr/bin/env python3
import os
brokerhost = os.environ['REDIS_URL']

class Config(object):
    DEBUG = True
    
class Broker(Config):
    BROKER_NAME = 'Redis'
    BROKER_URL = 'redis://{}:6379/0'.format(brokerhost)
    broker_url = 'redis://{}:6379/0'.format(brokerhost)
    result_backend = 'redis://{}:6379/0'.format(brokerhost)
    