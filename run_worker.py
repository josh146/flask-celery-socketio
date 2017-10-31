#!/usr/bin/env python3

from app import celery

if __name__ == "__main__":
    argv = ['celery','worker','-l','info']
    celery.start(argv=argv)
