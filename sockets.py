from flask import session
from flask_socketio import send, emit, join_room, leave_room, ConnectionRefusedError
import app
import chat
import user

MESSAGES_PER_LOAD = 20

@app.socketio.on("connect")
def connect(auth):
    if not (user.logged_in() and chat.has_auth(chat.get_current_chat_id(), user.user_id())):
        raise ConnectionRefusedError("unauthorized")

    join_room(chat.get_current_chat_id())
    chat.set_present(chat_id=session["chat_id"], user_id=session["user_id"], present=True)
    emit("status", [{"id": user.user_id(), "online": True}], to=chat.get_current_chat_id())
    emit("messages", {"old": True, "messages": chat.get_messages(chat.get_current_chat_id(), MESSAGES_PER_LOAD)})

@app.socketio.on("disconnect")
def disconnect():
    chat.set_present(chat_id=session["chat_id"], user_id=session["user_id"], present=False)
    emit("status", [{"id": user.user_id(), "online": False}], to=chat.get_current_chat_id())