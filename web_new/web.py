#!/usr/bin/python3
"""Managing the web pages"""
import os
import requests
import secrets
from flask import Flask, render_template, request, make_response, abort
from flask import redirect, url_for
from flask_wtf.csrf import CSRFProtect
from web_new import api_requests


app = Flask(__name__)
csrf = CSRFProtect(app)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
api_host = os.environ.get('API_HOST')
api_port = os.environ.get('API_PORT')


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    """Landing page"""
    products = api_requests.get_products().get('products')
    return render_template('default.html', products=products)

@app.route('/', strict_slashes=False, methods=['POST'])
@csrf.exempt
def login():
    """Login verification"""
    username = request.form.get('username')
    password = request.form.get('password')
    login_url = f'http://{api_host}:{api_port}/api/v1_0/token/auth'
    
    if not username or not password:
        return {'error': 'Incorrect Username or Password'}, 400
    
    try:
        api_response = requests.post(login_url,
                                     json={'username': username,
                                           'password': password}, timeout=5)
        api_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    
    products = api_requests.get_products().get('products')
    access_token = api_response.json()['access_token']
    response = make_response(render_template('index.html', products=products))
    response.set_cookie('access_token', access_token, httponly=True,
                        secure=True)
    return response

@app.route('/cart', strict_slashes=False, methods=['POST', 'GET', 'PUT',
                                                   'DELETE'])
def add_cart():
    """saving the users cart items to db"""
    access_token = request.cookies.get('access_token')
    headers = {"Authorization": f'Bearer {access_token}',
               "Content_Type": "Application/json"}
    if request.method == 'POST':
        payload = request.get_json()
        response = api_requests.add_cart(payload, headers)
        return response
    if request.method == 'GET':
        response = api_requests.get_cart(headers)
        return response
    if request.method == 'PUT':
        quantity = request.get_json().get('quantity')
        product_id = request.get_json().get('product_id')
        if not quantity or not product_id:
            abort(400)
        response = api_requests.update_cart(quantity, product_id, headers)
        return response
    if request.method == 'DELETE':
        product_id = request.get_json().get('product_id')
        if not product_id:
            abort(400)
        response = api_requests.delete_cart(product_id, headers)
        return response
    
@app.route('/logout', strict_slashes=False)
def logout():
    '''Logging out'''
    return redirect(url_for('index'))


if __name__ == '__main__':
    host = os.environ.get('WEB_HOST')
    port = os.environ.get('WEB_PORT')
    app.run(host=host, port=port, debug=True)