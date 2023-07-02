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
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
