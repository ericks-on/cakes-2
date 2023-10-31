#!usr/bin/python3
"""Model for the API requests"""
import os
import requests
from dotenv import load_dotenv
from passlib.hash import bcrypt
from datetime import timedelta
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from models import storage
from models.user import User
from models.product import Product


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

def refresh_token(headers):
    """Refreshing access tokens"""
    current_user = get_jwt_identity()
    user = storage.get_user(current_user)
    if not user:
        return jsonify({"error": "Unauthorized", "status_code": 403})
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)

def get_products():
    """Get all products"""
    

def get_cart(headers):
    """Getting the items on cart"""
    try:
        cart_response = requests.get(cart_url, headers=headers, timeout=5)
        cart_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': err.response.text})
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection Error', 'status_code': 500})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request Timeout', 'status_code': 500})
    return jsonify(cart_response.json())

def add_cart(payload, headers):
    """Adding item to cart"""
    try:
        cart_response = requests.post(cart_url, json=payload,
                                      headers=headers, timeout=5)
        cart_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': err.response.text})
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection Error', 'status_code': 500})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request Timeout', 'status_code': 500})
    return jsonify(cart_response.json())

def update_cart(quantity, product_id, headers):
    """Updating item quantity on Cart"""
    url = cart_url + '/' + product_id
    try:
        response = requests.put(url=url, json={'quantity':quantity},
                                timeout=5, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': err.response.text})
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection Error', 'status_code': 500})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request Timeout', 'status_code': 500})
    return jsonify(response.json())

def delete_cart(product_id, headers):
    """Deleting item in cart"""
    url = cart_url + '/' + product_id
    try:
        response = requests.delete(url, timeout=5, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': err.response.text})
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection Error', 'status_code': 500})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request Timeout', 'status_code': 500})
    return jsonify(response.json())