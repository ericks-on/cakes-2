#!usr/bin/python3
"""Model for the API requests"""
import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_host = os.environ.get('API_HOST')
api_port = os.environ.get('API_PORT')
login_url = f'http://{api_host}:{api_port}/api/v1_0/token/auth'
products_url = f'http://{api_host}:{api_port}/api/v1_0/products'
cart_url = f'http://{api_host}:{api_port}/api/v1_0/cart'


def login(username, password):
    """Login verification"""
    try:
        api_response = requests.post(login_url,
                                     json={'username': username,
                                           'password': password}, timeout=5)
        api_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Request Timeout'}, 500
    return api_response.json(), 200

def get_products():
    """Get all products"""
    try:
        pdt_response = requests.get(products_url, timeout=5)
        pdt_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Request Timeout'}, 500
    return pdt_response.json(), 200

def get_cart(headers):
    """Getting the items on cart"""
    try:
        cart_response = requests.get(cart_url, headers=headers, timeout=5)
        cart_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Connection Error'}, 500
    return cart_response.json(), 200

def add_cart(payload, headers):
    """Adding item to cart"""
    try:
        cart_response = requests.post(cart_url, payload=payload,
                                      headers=headers, timeout=5)
        cart_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Connection Error'}, 500
    return cart_response.json(), 200

def update_cart(quantity, product_id, headers):
    """Updating item quantity on Cart"""
    url = cart_url + f'/<{product_id}>'
    try:
        response = requests.put(url=url, json={'quantity':quantity},
                                timeout=5, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Connection Error'}, 500
    return response.json(), 200

def delete_cart(product_id, headers):
    """Deleting item in cart"""
    url = cart_url + f'/<{product_id}>'
    try:
        response = requests.delete(url, timeout=5, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Connection Error'}, 500
    return response.json(), 200