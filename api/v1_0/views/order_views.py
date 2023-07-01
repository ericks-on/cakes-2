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


@orders_bp.route('/', methods=['GET'])
@jwt_required
@swag_from('documentation/order/all_orders.yml')
def all_orders():
    """To obtain all orders"""
    username = get_jwt_identity()
    user = storage.get_user(username)
    if user.user_type == 'admin':
        return storage.all(Order)
    return user.orders

@orders_bp.route('/<order_id>', methods=['GET'])
@swag_from('documentation/order/get_order_by_id.yml')
def get_order_by_id(order_id):
    """Getting order by id from url"""
    order = storage.get(Order, order_id)
    return jsonify(order.to_dict())


