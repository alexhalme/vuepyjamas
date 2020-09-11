#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import time, eventlet
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)



@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('inJS', namespace='/test')
def socketJS(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    print(message)

    message['lab'] = f'time is {int(time.time())}'

    emit('sendPy',
         message)




if __name__ == '__main__':
    socketio.run(app, debug=True)
