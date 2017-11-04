#!/usr/bin/env python3

from flask import Flask, Response, jsonify, flash, \
    render_template, url_for, request, session

from flask_socketio import SocketIO, emit, join_room, rooms

import eventlet

from tasks import submit_task, _current_state

eventlet.monkey_patch()

app = Flask(__name__)

app.config.from_object('config.Redis')

socketio = SocketIO(app,
    async_mode='eventlet',
    message_queue=app.config['BROKER_URL']
    )


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/run')
def connect():
    user_id = request.sid
    session['user_id'] = user_id

    if user_id:
        join_room(user_id)

    msg = {'status': 'Connected user', 'user_id': user_id}
    emit('connected', msg, room=user_id)


@socketio.on('submit', namespace='/run')
def submit(msg):
    user_id = msg['user_id']
    bar_id = msg['bar_id']

    task = submit_task.apply_async(args=[user_id,bar_id], queue='socketIO')
    print(user_id)

    state = _current_state('PENDING', task.id, bar_id, 0, 1, 'Job pending...')
    emit('event', state, room=user_id)


@socketio.on('cancel', namespace='/run')
def cancel_task(msg):
    user_id = msg['user_id']
    task_id = msg['task_id']
    bar_id = msg['bar_id']

    task = submit_task.AsyncResult(task_id)
    task.revoke(terminate=True)

    state = _current_state('REVOKED', task_id, bar_id, 1, 1, 'Canceled')
    emit('event', state, room=user_id)


if __name__ == "__main__":
    socketio.run(app, debug=True)
