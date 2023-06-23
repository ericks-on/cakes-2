#!/usr/bin/python3
"""the views"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/1.0')
