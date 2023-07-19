from flask_socketio import SocketIO, emit
from flask import request
from dotenv import load_dotenv
import requests
import os


load_dotenv()
socketio = SocketIO()
host = os.getenv('KIMUKA_API_HOST')
port = os.getenv('KIMUKA_API_PORT')


@socketio.on('connect')
def test_connect():
    """test connection"""
    print('Client connected')

@socketio.on('message')
def handle_message(msg):
    """handle message"""
    print('Message: ' + msg)

@socketio.on('json')
def handle_json(json):
    """handle json"""
    print('json: ' + str(json))

@socketio.on('client_send')
def handle_send_message(msg):
    """handle send message"""
    print('Message: ' + msg)
    access_token = request.cookies.get('access_token_cookie')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_url = f"http://{host}:{port}/api/v1_0/users/self"
    try:
        user_response = requests.get(user_url, headers=headers).json()
    except Exception as error:
        print(error)
        return
    try:
        user = user_response['user']
    except Exception as error:
        print(error)
        return
    sender = user['user_type']
    json = {'sender': sender, 'message': msg}
    emit('chat', json, broadcast=True)
