#!/usr/bin/python3
"""Managing the web pages"""
import os
import requests
from flask import Flask, render_template, request, make_response


app = Flask(__name__)
api_host = os.environ.get('API_HOST')
api_port = os.environ.get('API_PORT')


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    """Landing page"""
    return render_template('default.html')

@app.route('/', strict_slashes=False, methods=['POST'])
def login():
    """Login verification"""
    username = request.form.get('username')
    password = request.form.get('password')
    login_url = 'http://{}:{}/api/v1_0/token/auth'.format(api_host, api_port)
    
    if not username or not password:
        return {'error': 'Incorrect Username or Password'}, 400
    
    try:
        api_response = requests.post(login_url,
                                     json={'username': username,
                                           'password': password}, timeout=5)
        api_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    access_token = api_response.json()['access_token']
    response = make_response(render_template('index.html'))
    response.set_cookie('access_token', access_token, httponly=True)
    return response


if __name__ == '__main__':
    host = os.environ.get('WEB_HOST')
    port = os.environ.get('WEB_PORT')
    app.run(host=host, port=port, debug=True)