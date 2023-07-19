from flask_socketio import SocketIO, emit, send

socketio = SocketIO()


@socketio.on('connect')
def test_connect():
    """test connection"""
    print('Client connected')

@socketio.on('message')
def handle_message(msg):
    """handle message"""
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('json')
def handle_json(json):
    """handle json"""
    print('json: ' + str(json))
