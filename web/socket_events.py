from flask_socketio import SocketIO, emit, join_room
from flask import request, abort
from dotenv import load_dotenv
import requests
import os


load_dotenv()
socketio = SocketIO()
host = os.getenv('KIMUKA_API_HOST')
port = os.getenv('KIMUKA_API_PORT')


@socketio.on('connect', namespace='/client')
def test_connect():
    """test connection and authentication"""
    access_token = request.cookies.get('access_token_cookie')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_url = f"http://{host}:{port}/api/v1_0/users/self"
    try:
        user_response = requests.get(user_url, headers=headers,
                                     timeout=5).json()
    except requests.exceptions.ConnectionError as error:
        abort(500, description=error)
    except ValueError as error:
        abort(400, description=error)
    except Exception as error:
        abort(500, description=error)
    try:
        user = user_response['user']
    except Exception as error:
        abort(401, description=error)
    if user["user_type"] == "admin":
        name_space = '/admin'
        join_room(name_space)
    else:
        client_namespace = '/' + user['username']
        join_room(client_namespace)
        print(f'Client {user["username"]} added to room {client_namespace}')

    print(f'User {user["username"]} connected')

@socketio.on('connect', namespace='/admin')
def test_connect_admin():
    """test connection and authentication"""
    access_token = request.cookies.get('access_token_cookie')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_url = f"http://{host}:{port}/api/v1_0/users/self"
    try:
        user_response = requests.get(user_url, headers=headers,
                                     timeout=5).json()
    except requests.exceptions.ConnectionError as error:
        abort(500, description=error)
    except ValueError as error:
        abort(400, description=error)
    except Exception as error:
        abort(500, description=error)
    try:
        user = user_response['user']
    except Exception as error:
        abort(401, description=error)
    if user["user_type"] == "admin":
        name_space = '/admin'
        join_room(name_space)
    else:
        abort(403, description="You are not admin")

    print(f'User {user["username"]} connected')

@socketio.on('message')
def handle_message(msg):
    """handle message"""
    print('Message: ' + msg)

@socketio.on('json')
def handle_json(json):
    """handle json"""
    print('json: ' + str(json))

@socketio.on('send', namespace='/client')
def handle_send_message(json):
    """handle send message"""
    print('Message: ' + json["msg"])
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
    sender = user['username']
    json = {'sender': sender, 'msg': json["msg"]}
    print(json["sender"])
    emit('from_client', json, namespace='/admin', to='/admin')

@socketio.on('send', namespace='/admin')
def handle_to_admin(json):
    """handle to admin"""
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
    if user["user_type"] == "admin":
        sender = 'Admin'
        json = {'sender': sender, 'msg': json["msg"]}
        print(json["sender"])
        emit('recieve', json, to='/erickson', namespace='/client')
    else:
        abort(403, description="You are not admin")