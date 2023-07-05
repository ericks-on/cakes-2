#!/usr/bin/python3
"""Flask appp to manage web pages"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def index():
    """This is the route for landing page"""
    return render_template('index.html', urlFor=url_for)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Handles login"""
    if request.method == 'GET':
        return render_template('index.html', urlFor=url_for)
    else:
        url = "http://192.168.0.34:3000/api/v1_0/login"
        payload = {}
        payload["username"] = request.form["username"]
        payload["password"] = request.form["password"]
        headers = {"Content-Type": "application/json"}
        api_response = requests.post(url=url, json=payload, headers=headers)
        response_obj = api_response.json()
        if api_response.status_code == 200:
            response = redirect("http://0.0.0.0:5000/user")
            response.headers["Authorization"] = "Bearer " + response_obj["access_token"]
            return response
        else:
            return render_template('index.html', urlFor=url_for)
        
@app.route("/user")
def user_page():
    """the user page"""
    return render_template('user.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
