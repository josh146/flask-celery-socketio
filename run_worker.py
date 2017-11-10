#!/usr/bin/env python3

from tasks import celery

if __name__ == "__main__":
    argv = ['celery','worker','-l','DEBUG','-c','8','-Q','socketIO']
    celery.start(argv=argv)
