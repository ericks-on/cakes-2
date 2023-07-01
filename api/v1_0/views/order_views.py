#!/usr/bin/python3
"""Contains views for orders"""
from flask import Blueprint, jsonify
from flasgger.utils import swag_from
from models import storage
from models.order import Order
from models.user import User
import os
from flask_jwt_extended import get_jwt_identity, jwt_required


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/<user_id>', methods=['GET'])
@swag_from('documentation/orders.yml')
def index(user_id):
    """To obtain all orders"""
    user = storage.get(User, user_id)
    obj_dicts = []
    if user.user_type == 'admin':
        orders = storage.all(Order)
    else:
        orders = user.orders
    for obj in orders:
        obj_dicts.append(obj.to_dict())
    return jsonify(obj_dicts)

@orders_bp.route('/<order_id>', methods=['GET'])
@swag_from('documentation/orders.yml')
def get_order_by_id(order_id):
    """Getting order by id from url"""
    order = storage.get(Order, order_id)
    return jsonify(order.to_dict())


