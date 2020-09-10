#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import time
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)

socketio = SocketIO(app, async_mode='eventlet')

#https://stackoverflow.com/questions/40460846/using-flask-inside-class
class Vuepyjama:
    def __init__(self, namespace):
        self.namespace = namespace
    '''
    @staticmethod
    @app.route('/<kw>')
    def getget(kw):
        print(f'kw:{kw}')
        if self.namespace == kw:
            return render_template('index.html', async_mode=socketio.async_mode)
    '''




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
