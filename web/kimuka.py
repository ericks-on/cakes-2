#!/usr/bin/python3
"""Flask appp to manage web pages"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import make_response
from flask_jwt_extended import jwt_required, JWTManager
import requests
import os
from datetime import datetime


app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('KIMUKA_API_SEC_KEY')
host = os.environ.get('KIMUKA_API_HOST')
port = os.environ.get('KIMUKA_API_PORT')


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
        url = f"http://{host}:{port}/api/v1_0/login"
        payload = {}
        payload["username"] = request.form["username"]
        payload["password"] = request.form["password"]
        headers = {"Content-Type": "application/json"}
        api_response = requests.post(url=url, json=payload,
                                     headers=headers, timeout=5)
        response_obj = api_response.json()
        if api_response.status_code == 200:
            response = make_response(redirect(url_for('user_page')))
            response.headers["Authorization"] = "Bearer " + response_obj["access_token"]
            return response
        elif api_response.status_code == 401:
            return redirect(url_for('index'))
        
@app.route("/user", methods=['GET'])
@jwt_required()
def user_page():
    """the user page"""
    return render_template('user.html', urlFor=url_for)

@app.route("/order", methods=['GET'])
def order_page():
    """the order page"""
    orders_url = f"http://{host}:{port}/api/v1_0/orders"
    orders_response = requests.get(url=orders_url, timeout=5).json()
    orders = orders_response["orders"]
    order_history = orders[0:10]
    return render_template('orders.html', urlFor=url_for,
                           orders=orders, order_history=order_history
                           )

@app.route("/sales", methods=['GET'])
def get_sales():
    """get sales for popup"""
    year = datetime.now().year
    url = f"http://{host}:{port}/api/v1_0/products/sales/total/{year}"
    api_response = requests.get(url=url, timeout=5).json()
    return jsonify(api_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
