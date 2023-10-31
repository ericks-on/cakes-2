#!/usr/bin/python3
"""Managing the web pages"""
import os
from dotenv import load_dotenv
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
from flask_jwt_extended import unset_access_cookies
from flask_cors import CORS
from web_new import storage


load_dotenv()
app = Flask(__name__)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# secret_key = secrets.token_hex(16)
secret_key = os.environ.get('KIMUKA_SECRET_KEY')
jwt_key = os.environ.get('KIMUKA_JWT_KEY')
app.config['SECRET_KEY'] = secret_key
app.config['JWT_SECRET_KEY'] = jwt_key
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
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
            access_token = request.cookies.get('access_token_cookie')
            headers = {
                "Authorization": f'Bearer {access_token}',
                "X-CSRFToken": generate_csrf()
                }
            refresh_response = storage.refresh_token(headers)
            if not refresh_response.get_json().get('error'):
                access_token = refresh_response.get_json().get('access_token')
                set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
    
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    """what happens when no token is present"""   
    print(callback)
    return redirect(url_for('index'), 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    """What happens when token is invalid"""
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(url_for('index')))
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(header, payload):
    """What happens when token is expired"""
    # Expired auth header
    resp = make_response(redirect(url_for('index')))
    unset_access_cookies(resp)
    return resp, 302

@app.route('/', strict_slashes=False, methods=['GET'])
@csrf.exempt
def index():
    """Landing page"""
    products = storage.get_products().get_json().get('products')
    if not products:
        message = "error fetching the products"
        return render_template('default.html', products=[],
                               error=message)
    return render_template('default.html', products=products)

@app.route('/', strict_slashes=False, methods=['POST'])
@csrf.exempt
def login():
    """Login verification"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return {'error': 'Incorrect Username or Password'}, 400
    return_obj = storage.login(username, password).get_json()
    if not return_obj.get('error'):
        access_token = return_obj.get('access_token')
        response = make_response(redirect(url_for('home')))
        set_access_cookies(response, access_token)
        return response
    return return_obj, return_obj.get('status_code')

@app.route('/home', strict_slashes=False, methods=['GET'])
@jwt_required()
def home():
    """After login"""
    products = storage.get_products().get_json().get('products')
    return render_template('index.html', products=products)

@app.route('/cart', strict_slashes=False, methods=['POST', 'GET', 'PUT',
                                                   'DELETE'])
@jwt_required()
def cart():
    """CRUD operations on cart"""
    access_token = request.cookies.get('access_token_cookie')
    headers = {
        "Authorization": f'Bearer {access_token}',
        "Content-Type": "Application/json",
        "X-CSRFToken": generate_csrf()
        }
    if request.method == 'POST':
        payload = request.get_json()
        response = storage.add_cart(payload, headers).get_json()
        return response
    if request.method == 'GET':
        headers = {"Authorization": f'Bearer {access_token}'}
        response = storage.get_cart(headers).get_json()
        return response
    if request.method == 'PUT':
        quantity = request.get_json().get('quantity')
        product_id = request.get_json().get('product_id')
        if not quantity or not product_id:
            abort(400)
        response = storage.update_cart(quantity, product_id,
                                            headers).get_json()
        return response
    if request.method == 'DELETE':
        product_id = request.get_json().get('product_id')
        if not product_id:
            abort(400)
        response = storage.delete_cart(product_id, headers).get_json()
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