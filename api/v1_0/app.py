#!/usr/bin/python3
"""This module contains the Donuts RESTFull API"""
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flasgger import Swagger
from api.v1_0.views import app_views
import os
from flask_jwt_extended import create_access_token, JWTManager
from passlib.hash import bcrypt
from models.user import User
from datetime import timedelta
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest
from models import storage


load_dotenv()


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
Swagger(app)
app.config['SWAGGER'] = {
        'title': 'Kimuka RESTFull API'
        }
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('KIMUKA_API_SEC_KEY')
app.register_blueprint(app_views)


@app.route('/api/v1_0/login', methods=['POST'])
def login():
    """authenticates user and creates an access token"""
    all_users = storage.all(User)
    all_usernames = [user.username for user in all_users]
    try:
        username = request.get_json().get("username")
    except BadRequest:
        return jsonify({"msg": "Missing username parameter"}), 400
    try:
        password = request.get_json().get("password")
    except BadRequest:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username in all_usernames:
        user = storage.get_user(username)
        hashed_pwd = user.password
        if bcrypt.verify(password, hashed_pwd) is True:
            access_token = create_access_token(identity=username,
                                               expires_delta=timedelta(hours=1))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Wrong Username or Password"}), 401
    else:
        return jsonify({"msg": "Wrong Username or Password"}), 401


@app.teardown_appcontext
def teardown(exception=None):
    """calls storage close method to remove current session"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """defines what happens if code 404 is raised"""
    return make_response(jsonify({'error': 'Not Found'}), 400)


if __name__ == "__main__":
    hst = os.environ.get('KIMUKA_API_HOST')
    if not hst:
        hst = '0.0.0.0'
    prt = os.environ.get('KIMUKA_API_PORT')
    if not prt:
        prt = 3000
    app.run(host=hst, port = prt, debug=True)
