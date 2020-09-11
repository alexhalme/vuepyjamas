#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request,     copy_current_request_context, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import time, eventlet
from functools import partial, update_wrapper

#https://www.kisphp.com/python/flask-routes-in-class


# from link up -> allows @route decorator within fct
class Klask(Flask):

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

    def route(self, rule, **options):
        apply_self = lambda f: update_wrapper(partial(f, self=None), f)
        decorator = Flask.route(self, rule, **options)
        def compose(g, f):
            return lambda *args, **kwargs: g(f(*args, **kwargs))
        return compose(decorator, apply_self)

# assets -> good idea?
class assets():
    def __init__(self):
        self.jquery = 'https://code.jquery.com/jquery-1.12.4.min.js'
        self.socket = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js'
        self.nacl = 'static/nacl_alex.js'
        self.vue = 'https://cdn.jsdelivr.net/npm/vue/dist/vue.js'
        self.quasar = 'https://cdn.jsdelivr.net/npm/quasar@1.13.2/dist/quasar.umd.min.js'

# main fct
class Vuepyjamas(assets):

    def __init__(self, name, ioCallback):
        # create flask app and socket
        self.ioCallback = ioCallback
        self.flaskApp = Klask(name)
        self.socketio = SocketIO(self.flaskApp, async_mode=None)
        self.socketio.on_event('inJS', self.socketJS, namespace='/test')

        # flask router (for GET mainly, here to insert jinja stuff)
        @self.flaskApp.route("/")
        def hello(self):
            return render_template('index.html', async_mode=pyjamas.socketio.async_mode)

    # fct called when socket gets info
    def socketJS(self, socketIO):
        # pass data (socketIO) to ioCallback function (user defined) then send back data thru socket

        emit('sendPy', self.ioCallback(socketIO))

    # runs the socket
    def run(self):
        self.socketio.run(self.flaskApp, debug=True)

    # flask app getter
    def getFlaskApp(self):
        return self.flaskApp


def myCustomFct(message):
    print(message)
    message['lab'] = f'time is {int(time.time())}'
    return message


# declare the Vuepyjamas object
pyjamas = Vuepyjamas(__name__, myCustomFct)
# no clue why but must REGISTER globally this damn object
flaskApp = pyjamas.getFlaskApp()




if __name__ == "__main__":
    # run the app
    pyjamas.run(debug=True)

