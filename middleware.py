from flask_socketio import SocketIO
from events import events_to_register

socketio = SocketIO()


def init_app(app):
    socketio.init_app(app)
    for name_event, event_action in events_to_register:
        socketio.on_event(name_event, event_action)


def start_app(app):
    socketio.run(app)
