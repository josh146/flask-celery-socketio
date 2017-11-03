#!/usr/bin/env python3

class Config(object):
    DEBUG = True
    
class Redis(Config):
    BROKER_NAME = 'Redis'
    BROKER_URL = 'redis://127.0.0.1:6379/0'
    broker_url = 'redis://127.0.0.1:6379/0'
    result_backend = 'redis://127.0.0.1:6379/0'

class AWSElastiCache(Config):
    BROKER_NAME = 'AWSElastiCache'
    BROKER_URL = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
    broker_url = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
    result_backend = 'redis://redis-server.xdgpw9.0001.use1.cache.amazonaws.com:6379'
