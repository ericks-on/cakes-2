#!/usr/bin/python3
"""Flask appp to manage web pages"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def index():
    """This is the route for landing page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Handles login"""
    url = "http//0.0.0.0:3000/api/v1_0/login"
    payload = {}
    payload["username"] = request.form["username"]
    payload["password"] = request.form["password"]
    return jsonify(payload)
    # api_response = requests.post(url=url, data=payload)
    # if api_response.status_code == 200:
    #     response = redirect("http://0.0.0.0:5000/user")
    #     response.headers["Authorization"] = "Bearer " + api_response.text()
    #     return response
    # else:
    #     return redirect(url_for('index'))
    
@app.route("/user")
def user_page():
    """the user page"""
    return render_template('user.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
