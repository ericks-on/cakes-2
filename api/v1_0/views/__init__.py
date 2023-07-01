#!/usr/bin/python3
"""the views"""
from flask import Blueprint
from api.v1_0.views.order_views import orders_bp


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1_0')
app_views.register_blueprint(orders_bp)
