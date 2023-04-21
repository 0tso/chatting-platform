from flask import session
from flask_socketio import send, emit, join_room, leave_room, ConnectionRefusedError
import app
import chat
import user

@app.socketio.on("connect")
def connect(auth):
    if not (user.logged_in() and chat.has_auth(chat.get_current_chat_id(), user.user_id())):
        raise ConnectionRefusedError("unauthorized")

    join_room(chat.get_current_chat_id())
    chat.set_present(chat_id=session["chat_id"], user_id=session["user_id"], present=True)
    emit("status", [{"id": user.user_id(), "online": True}], to=chat.get_current_chat_id())

@app.socketio.on("disconnect")
def disconnect():
    chat.set_present(chat_id=session["chat_id"], user_id=session["user_id"], present=False)
    emit("status", [{"id": user.user_id(), "online": False}], to=chat.get_current_chat_id())