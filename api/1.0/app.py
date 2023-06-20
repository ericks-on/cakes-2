#!/usr/bin/python3
"""This module contains the Donuts RESTFull API"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from models import storage
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
Swagger(app)
app.config['SWAGGER'] = {
        'title': 'Donuts RESTFull API'
        }


@app.teardown_appcontext
def teardown(exception=None):
    """calls storage close method to remove current session"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """defines what happens if code 404 is raised"""
    return make_response(jsonify({'error': 'Not Found'}))


if __name__ == "__main__":
    hst = os.environ.get('CAKES_API_HOST')
    if not hst:
        hst = '0.0.0.0'
    prt = os.environ.get('CAKES_API_PORT')
    if not prt:
        prt = 5000
    app.run(host=hst, port = prt)
