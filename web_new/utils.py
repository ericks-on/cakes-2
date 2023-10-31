#!usr/bin/python3
"""Functions to retrieve data from storage"""
from dotenv import load_dotenv
from passlib.hash import bcrypt
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from models import storage
from models.user import User
from models.product import Product
from models.cart import Cart


load_dotenv()


def login(username, password):
    """Login verification"""
    all_users = storage.all(User)
    all_usernames = [user.username for user in all_users]
    if not username or not password:
        return jsonify({"msg": "Missing username parameter"}), 400

    if username in all_usernames:
        user = storage.get_user(username)
        hashed_pwd = user.password
        if bcrypt.verify(password, hashed_pwd) is True:
            access_token = create_access_token(identity=username, fresh=True)
            return jsonify(access_token=access_token)
        return jsonify({"error": "Wrong Username or Password",
                        "status_code": 401})
    return jsonify({"error": "Wrong Username or Password",
                    "status_code": 401})

def refresh_token():
    """Refreshing access tokens"""
    current_user = get_jwt_identity()
    user = storage.get_user(current_user)
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)

def get_products():
    """Get all products"""
    products = [item.to_dict() for item in storage.all(Product)]
    return jsonify({"products": products})

def get_cart():
    """Getting the items on cart"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    cart_items = [item for item in storage.all(Cart)
                  if item.user_id == user.id]
    cart = [{"product_id": item.product_id,
             "quantity": item.quantity,
             "name": storage.get(Product, item.product_id).name,
             "price": storage.get(Product, item.product_id).price,
             "image": storage.get(Product, item.product_id).image
             } for item in cart_items]
    return jsonify({"cart": cart})

def add_cart(payload):
    """Adding item to cart"""
    product_id = payload.get('product_id')
    quantity = payload.get('quantity')
    print(payload)
    user = storage.get_user(get_jwt_identity())
    product = storage.get(Product, product_id)
    if not product:
        return jsonify({"error": "Not Found", "status_code": 404})
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    if not product_id or not quantity:
        return jsonify({"error": "Bad Request", "status_code": 400})
    
    new_item = Cart(product_id=product_id, quantity=quantity, user_id=user.id)
    storage.add(new_item)
    storage.save()
    return jsonify({product.name: new_item.to_dict()})

def update_cart(quantity, product_id):
    """Updating item quantity on Cart"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    cart = [item for item in storage.all(Cart)
            if item.user_id == user.id]
    product_name = storage.get(Product, product_id)
    for item in cart:
        if item.product_id == product_id:
            item.quantity = quantity
            storage.save()
            return jsonify({product_name: item.to_dict()})
    return jsonify({"error": "Not Found", "status_code": 404})

def delete_cart(product_id):
    """Deleting item in cart"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    product_ids = [item.product_id for item in storage.all(Cart)
                   if item.user_id == user.id]
    if product_id not in product_ids:
        return jsonify({"error": "Not Found", "status_code": 404})
    cart = [item for item in storage.all(Cart)
            if item.user_id == user.id]
    product = storage.get(Product, product_id)    
    for item in cart:
        if item.product_id == product_id:
            storage.delete(item)
            storage.save()
            return jsonify({product.name: {}})