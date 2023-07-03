#!/usr/bin/python3
"""Flask appp to manage web pages"""
from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def index():
    """This is the route for landing page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Handles login"""
    url = "http//0.0.0.0:5000/api/v1_0/login"
    payload = {}
    payload["username"] = request.form["username"]
    payload["password"] = request.form["password"]
    api_response = requests.post(url=url, data=payload)
    if api_response.status_code == 200:
        response = redirect("http://0.0.0.0:5000/api.v1_0/user")
        response.headers["Authorization"] = "Bearer " + api_response.text()
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
