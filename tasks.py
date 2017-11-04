#!/usr/bin/env python3
import numpy as np
from numpy.random import choice, random, randint
import time

from celery import Celery
from celery.task.control import revoke

from flask_socketio import SocketIO

celery = Celery(__name__)
celery.config_from_object('config.Redis')


def _current_state(state, tid, bid, current, total, status, result=None):
    tmp = {
        'task_id': tid,
        'bar_id': bid,
        'data': {
            'state': state,
            'current': current,
            'total': total,
            'status': status,
            'result': None
        }
    }

    return tmp


@celery.task(bind=True)
def submit_task(self, user_id, bar_id):
    """Background task that runs a long function with progress reports."""
    socketio = SocketIO(message_queue=celery.conf.broker_url)

    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''

    total = randint(10, 50)

    for i in range(total):
        if not message or random() < 0.25:
            message = '{0} {1} {2}...'.format(
                choice(verb), choice(adjective), choice(noun))

        state = _current_state('PROGRESS', self.request.id, bar_id, i, total, message)
        socketio.emit('event', state, room=user_id, namespace='/run')
        time.sleep(1)

    state = _current_state('SUCCESS', self.request.id, bar_id, 1, 1, 'Complete!', 42)
    socketio.emit('event', state, room=user_id, namespace='/run')

