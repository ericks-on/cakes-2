#!/usr/bin/python3
"""the views"""
from flask import Blueprint
from api.v1_0.views.order_views import orders_bp
from api.v1_0.views.product_views import products_bp
from api.v1_0.views.user_views import user_bp
from api.v1_0.views.chat_views import chat_bp


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1_0')
app_views.register_blueprint(orders_bp)
app_views.register_blueprint(products_bp)
app_views.register_blueprint(user_bp)
app_views.register_blueprint(chat_bp)
