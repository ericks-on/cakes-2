#!usr/bin/python3
"""Model for the API requests"""
import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_host = os.environ.get('API_HOST')
api_port = os.environ.get('API_PORT')
login_url = 'http://{}:{}/api/v1_0/token/auth'.format(api_host, api_port)
products_url = 'http://{}:{}/api/v1_0/products'.format(api_host, api_port)


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

def new_order()