#!/usr/bin/python3
"""Managing the web pages"""
import os
import secrets
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dotenv import load_dotenv
from flask import Flask, render_template, request, make_response, abort
from flask import redirect, url_for, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
from flask_jwt_extended import unset_access_cookies
from flask_jwt_extended import get_jwt_identity
from flask_cors import CORS
from web import utils
from models import storage
from models.product import Product
from web.forms import ProductsForm
from models.notification import Notification


load_dotenv()
app = Flask(__name__)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
secret_key = secrets.token_hex(16)
# secret_key = os.environ.get('KIMUKA_SECRET_KEY')
# jwt_key = os.environ.get('KIMUKA_JWT_KEY')
app.config['SECRET_KEY'] = secret_key
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


@app.after_request
def refresh_expiring_jwts(response):
    """refreshing jwt tokens"""
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = request.cookies.get('access_token_cookie')
            refresh_response = utils.refresh_token()
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
    print(callback)
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
    products = utils.get_products().get_json().get('products')
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
    return_obj = utils.login(username, password).get_json()
    if not return_obj.get('error'):
        access_token = return_obj.get('access_token')
        if return_obj.get('user_type') == 'admin':
            response = make_response(redirect(url_for('admin')))
        else:
            response = make_response(redirect(url_for('home')))
        set_access_cookies(response, access_token)
        return response
    return return_obj, return_obj.get('status_code')

@app.route('/home', strict_slashes=False, methods=['GET'])
@jwt_required()
def home():
    """After login"""
    user_details = storage.get_user(get_jwt_identity()).to_dict()
    products = utils.get_products().get_json().get('products')
    return render_template('index.html', products=products,
                           user_details=user_details)
    
@app.route('/admin', strict_slashes=False, methods=['GET'])
@jwt_required()
def admin():
    """The admin page"""
    user = storage.get_user(get_jwt_identity())
    user_details = storage.get_user(get_jwt_identity()).to_dict()
    products_form = ProductsForm()
    if user.user_type != "admin":
        abort(403)
    
    products = [item.to_dict() for item in storage.all(Product)]
    notifications = [item.to_dict() for item in storage.all(Notification)]
    return render_template('admin.html', user_details=user_details,
                           products_form=products_form, products=products,
                           notifications=notifications)

@app.route('/cart', strict_slashes=False, methods=['POST', 'GET', 'PUT',
                                                   'DELETE'])
@jwt_required()
def cart():
    """CRUD operations on cart"""
    if request.method == 'POST':
        payload = request.get_json()
        response = utils.add_cart(payload).get_json()
        return response
    if request.method == 'GET':
        response = utils.get_cart().get_json()
        return response
    if request.method == 'PUT':
        quantity = request.get_json().get('quantity')
        product_id = request.get_json().get('product_id')
        if not quantity or not product_id:
            abort(400)
        response = utils.update_cart(quantity, product_id).get_json()
        return response
    if request.method == 'DELETE':
        product_id = request.get_json().get('product_id')
        if not product_id:
            abort(400)
        response = utils.delete_cart(product_id).get_json()
        return response
    
@app.route('/logout', strict_slashes=False)
def logout():
    '''Logging out'''
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response

@app.route('/products', strict_slashes=False, methods=['DELETE', 'POST',
                                                       'PUT'])
@jwt_required()
def add_products():
    """Adding new products"""
    user = storage.get_user(get_jwt_identity())
    if user.user_type != 'admin':
        abort(403)
    if request.method == 'POST':
        name = request.get_json().get('name')
        price = request.get_json().get('price')
        image = 'donut.jpg'
        if not name or not price:
            return jsonify({"error": "Bad Request", "status_code": 400}), 400
        new_pdt = Product(name=name, price=price, image=image)
        storage.add(new_pdt)
        storage.save()
        product = storage.get_product(name)
        return jsonify(product.to_dict()), 201
    if request.method == 'PUT':
        name = request.get_json().get('name')
        price = request.get_json().get('price')
        id_ = request.get_json().get('id')
        if not name or not price or not id_:
            return jsonify({"error": "Bad Request"}), 400
        product = storage.get(Product, id_)
        if not product:
            return jsonify({"error": "Not Found"}), 404
        product.name = name
        product.price = price
        storage.save()
        return jsonify(storage.get_product(name).to_dict()), 200
    
@app.route('/notifications', strict_slashes=False, methods=['POST'])
@jwt_required()
def add_notifications():
    """add notifications"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(404)
    if user.user_type != 'admin':
        abort(403)
    message = request.get_json().get('message')
    if not message:
        return jsonify({"error": "Bad Request"}), 400
    notification = Notification(message=message)
    storage.add(notification)
    storage.save()
    return jsonify(storage.get(Notification, notification.id).to_dict()), 201


if __name__ == '__main__':
    host = os.environ.get('WEB_HOST')
    port = os.environ.get('WEB_PORT')
    app.run(host=host, port=port, debug=True)