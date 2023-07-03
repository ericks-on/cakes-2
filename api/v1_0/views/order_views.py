#!/usr/bin/python3
"""Contains views for orders"""
from flask import Blueprint, jsonify, abort, request
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
    return jsonify(user.orders)

@orders_bp.route('/', methods=['POST'])
@jwt_required
@swag_from('documentation/order/add_order.yml')
def add_order():
    """ Adds new order"""
    username = get_jwt_identity()
    user_id = storage.get_user(username).id
    order_value = request.json.get("order_value")
    quantity = request.json.get("quantity")
    new_order = Order(user_id=user_id, order_value=order_value, quantity=quantity)
    storage.add(new_order)
    storage.save()
    return jsonify(new_order.to_dict()), 200

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required
@swag_from('documentation/order/get_order_by_id.yml')
def get_order_by_id(order_id):
    """Getting order by id from url"""
    username = get_jwt_identity()
    user = storage.get_user(username)
    if user.user_type == 'admin':
        order = storage.get(Order, order_id)
    else:
        orders = [order for order in user.orders if order.id == order_id]
        if orders[0]:
            order = orders[0]
        else:
            order = None
    if order:
        r_order = order.to_dict()
        if r_order.status == 'completedd':
            r_order.status = 'settled'
        return jsonify(r_order)
    else:
        abort(404)

@orders_bp.route('/<order_id>', methods=['PUT'])
@jwt_required
@swag_from('documentation/order/update_order.yml')
def update_order(order_id):
    """updates order"""
    username = get_jwt_identity()
    user = storage.get_user(username)
    if user.user_type == 'admin':
        order = storage.get(Order, order_id)
    else:
        orders = user.orders
        for obj in orders:
            if obj.id == order_id:
                order = obj
            else:
                order = None
    if order:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify({'error': 'Invalid JSON data'}), 400
        for k, v in data.items():
            if k == 'status' and v not in ['pending',
                                           'confirmed',
                                           'delivered',
                                           'completedd']:
                return jsonify({'error': 'Bad Request'}), 400
            else:
                setattr(order, k, v)
        storage.save()
    else:
        abort(404)

@orders_bp.route('/<order_id>', methods=['DELETE'])
@jwt_required
@swag_from('documentation/order/delete_order.yml')
def delete_order(order_id):
    """Deleting order"""
    username = get_jwt_identity()
    user = storage.get_user(username)
    if user.user_type == 'admin':
        order = storage.get(Order, order_id)
    else:
        orders = user.orders
        for obj in orders:
            if obj.id == order_id:
                order = obj
            else:
                order = None
    if order:
        storage.delete(order)
        storage.save()
        return jsonify({}), 204
    else:
        abort(404)

