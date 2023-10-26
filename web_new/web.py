#!/usr/bin/python3
"""Managing the web pages"""
import os
import requests
import secrets
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask import Flask, render_template, request, make_response, abort
from flask import redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
from web_new import api_requests


app = Flask(__name__)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
api_host = os.environ.get('API_HOST')
api_port = os.environ.get('API_PORT')


@app.after_request
def refresh_expiring_jwts(response):
    """refreshing jwt tokens"""
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = api_requests.refresh_token().get('access_token')
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

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
    
    if not username or not password:
        return {'error': 'Incorrect Username or Password'}, 400
    login_response = api_requests.login(username, password)
    if not login_response.get('error'):
        access_token = login_response['access_token']
        response = make_response(redirect(url_for('home')))
        set_access_cookies(response, access_token)
        return response
    return login_response

@app.route('/home', strict_slashes=False, methods=['GET'])
@jwt_required()
def home():
    """After login"""
    products = api_requests.get_products().get('products')
    cart_csrf = generate_csrf()
    return render_template('index.html', products=products,
                           cart_csrf=cart_csrf)

@app.route('/cart', strict_slashes=False, methods=['POST', 'GET', 'PUT',
                                                   'DELETE'])
def cart():
    """CRUD operations on cart"""
    access_token = request.cookies.get('access_token')
    headers = {"Authorization": f'Bearer {access_token}',
               "Content-Type": "Application/json"}
    if request.method == 'POST':
        payload = request.get_json()
        response = api_requests.add_cart(payload, headers)
        return response
    if request.method == 'GET':
        headers = {"Authorization": f'Bearer {access_token}'}
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
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response


if __name__ == '__main__':
    host = os.environ.get('WEB_HOST')
    port = os.environ.get('WEB_PORT')
    app.run(host=host, port=port, debug=True)