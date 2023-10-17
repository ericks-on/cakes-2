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
    return api_response.json()

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
    return pdt_response.json()

def get_cart():
    """Getting the items on cart"""
    try:
        cart_response = requests.get(cart_url, timeout=5)
        cart_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'error': err.response.text}, err.response.status_code
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection Error'}, 500
    except requests.exceptions.Timeout:
        return {'error': 'Connection Error'}, 500
    return cart_response.json()

def add_cart(product_id, quantity):
    """Adding item to cart"""
    payload = {'quantity': quantity,
               'product_id': product_id}
    try:
        cart_response = requests.post(cart_url, payload=payload, timeout=5)
        cart_response.raise_for_status()
        
        