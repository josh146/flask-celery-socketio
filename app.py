#!/usr/bin/env python3
import numpy as np
from numpy.random import choice, random, randint
import time

from flask import Flask, Response, jsonify, flash, \
    render_template, url_for, request

from celery import Celery
from celery.task.control import revoke


app = Flask(__name__)

app.config.from_object('config.Redis')
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



@celery.task(bind=True)
def submit_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''

    total = randint(10, 50)

    for i in range(total):
        if not message or random() < 0.25:
            message = '{0} {1} {2}...'.format(choice(verb),choice(adjective),choice(noun))

        self.update_state(state='PROGRESS',
                          meta={'current': i,
                                'total': total,
                                'status': message
                        })
        time.sleep(1)

    return {'current': 100, 'result': 42,
                'status': 'Task completed!', 'total': 100}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    task = submit_task.apply_async()
    task_info = {
        'Location': url_for('taskstatus',task_id=task.id),
        'id': task.id
        }
    return jsonify({}), 202, task_info


@app.route('/cancel', methods=['POST'])
def cancel_task():
    task_id = request.get_json()['task_id']
    task = submit_task.AsyncResult(task_id)
    task.revoke(terminate=True)

    return jsonify({}), 202, ""


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = submit_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }

    elif task.state == 'REVOKED':
        # job terminated
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': "Job terminated",
            'result': "Job terminated"
        }

    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
        try:
            response['traceback'] = task.traceback.replace('\n', '<br>')
        except:
            pass

    return jsonify(response)


if __name__ == "__main__":
    app.run()
