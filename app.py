from flask import Flask
from os import getenv
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
socketio = SocketIO(app, ping_interval=int(getenv("SOCKETIO_PING_INTERVAL")), ping_timeout=int(getenv("SOCKETIO_TIMEOUT")))

import routes
import sockets

if __name__ == "__main__":
    socketio.run(app)