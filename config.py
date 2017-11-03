#!/usr/bin/env python3

class Config(object):
    DEBUG = True
    MESSAGE_BROKER = False
    
class Redis(Config):
    MESSAGE_BROKER = False
    BROKER_NAME = 'Redis'
    BROKER_URL = 'redis://127.0.0.1:6379/0'
    broker_url = 'redis://127.0.0.1:6379/0'
    result_backend = 'redis://127.0.0.1:6379/0'

class AWSElastiCache(Config):
    MESSAGE_BROKER = True
    BROKER_NAME = 'AWSElastiCache'
    BROKER_URL = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
    broker_url = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
    result_backend = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
