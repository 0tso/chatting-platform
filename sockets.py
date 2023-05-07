from flask import session
from flask_socketio import send, emit, join_room, ConnectionRefusedError
import app
import chat
import user

MESSAGES_PER_LOAD = 25
MAX_MESSAGE_LENGTH = 2000

def load_old_messages(pivot_message_id=None):
    messages = chat.get_messages(chat.get_current_chat_id(), MESSAGES_PER_LOAD, pivot_message_id)

    data = {"old": True, "messages": messages}
    if len(messages) == MESSAGES_PER_LOAD:
        data["remaining"] = True
    else:
        data["remaining"] = False
    return data


@app.socketio.on("connect")
def connect(auth):
    if not (user.logged_in() and chat.has_auth(chat.get_current_chat_id(), user.user_id())):
        raise ConnectionRefusedError("unauthorized")

    join_room(chat.get_current_chat_id())
    chat.set_present(chat_id=chat.get_current_chat_id(), user_id=user.user_id(), present=True)
    emit("status", [{"id": user.user_id(), "online": True}], to=chat.get_current_chat_id())
    emit("messages", load_old_messages())

@app.socketio.on("disconnect")
def disconnect():
    chat.set_present(chat_id=chat.get_current_chat_id(), user_id=user.user_id(), present=False)
    emit("status", [{"id": user.user_id(), "online": False}], to=chat.get_current_chat_id())

@app.socketio.event
def msg(message):
    if len(message) > MAX_MESSAGE_LENGTH:
        emit("error", f"Message length too long. Maximum length is {MAX_MESSAGE_LENGTH} characters.")
    else:
        id_and_time = chat.add_message(chat.get_current_chat_id(), user.user_id(), message)
        emit("messages", {"old": False, "messages": [id_and_time + (user.username(), message)]}, to=chat.get_current_chat_id())

@app.socketio.event
def load_messages(pivot_message_id):
    emit("messages", load_old_messages(pivot_message_id))