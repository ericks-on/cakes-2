#!/usr/bin/python3
"""Contains views for orders"""
from flask import Blueprint, jsonify, abort, request
from flasgger.utils import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from models.order import Order
from models.user import User
import os
import calendar
from models import storage


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['GET'])
@swag_from('documentation/order/all_orders.yml')
# @jwt_required()
def all_orders():
    """To obtain all orders"""
    # username = get_jwt_identity()
    username = 'erickson'
    user = storage.get_user(username)
    if user.user_type == 'admin':
        orders = [order.to_dict() for order in storage.all(Order)]
        return jsonify({"orders": orders}), 200
    else:
        orders = [order.to_dict() for order in user.orders]
        return jsonify({"orders": orders}), 200


@orders_bp.route('/', methods=['POST'])
@swag_from('documentation/order/add_order.yml')
@jwt_required()
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
@swag_from('documentation/order/get_order_by_id.yml')
@jwt_required()
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
@swag_from('documentation/order/update_order.yml')
@jwt_required()
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
        for key, val in data.items():
            if key == 'status' and val not in ['pending',
                                               'confirmed',
                                               'delivered',
                                               'completedd']:
                return jsonify({'error': 'Bad Request'}), 400
            else:
                setattr(order, key, val)
        storage.save()
    else:
        abort(404)

@orders_bp.route('/<order_id>', methods=['DELETE'])
@swag_from('documentation/order/delete_order.yml')
@jwt_required()
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

@orders_bp.route('/period/<year>/<month>', methods=['GET'])
@orders_bp.route('/period/<year>/', methods=['GET'])
@swag_from('documentation/order/get_order_by_period.yml')
# @jwt_required()
def get_order_by_period(year, month=None):
    """Getting order by period"""
    # username = get_jwt_identity()
    username = 'erickson'
    user = storage.get_user(username)
    if user.user_type == 'admin':
        orders = storage.all(Order)
    else:
        orders = user.orders

    if not orders:
        abort(404)

    if month:
        orders = [order for order in orders if
                  order.created_at.year == int(year)
                  and order.created_at.month == int(month)]
    else:
        orders = [order for order in orders
                  if order.created_at.year == int(year)]
    if orders:
        orders = [order.to_dict() for order in orders]
        return jsonify({"orders": orders}), 200
    else:
        abort(404)

@orders_bp.route('/totals/<year>', methods=['GET'])
@swag_from('documentation/order/get_order_totals.yml')
# @jwt_required()
def get_order_totals(year):
    """Getting order totals"""
    # username = get_jwt_identity()
    username = 'erickson'
    user = storage.get_user(username)
    if user.user_type == 'admin':
        orders = storage.all(Order)
    else:
        orders = user.orders
    if not orders:
        abort(404)
    orders = [order for order in orders if
              order.created_at.year == int(year)]
    if orders:
        months = calendar.month_name[1:]
        monthly_totals = {}
        for mon in months:
            month_totals = {}
            month_orders_total = len([order for order in orders if
                                      months[order.created_at.month - 1] ==
                                      mon])
            month_orders_value = sum([order.order_value for order in orders
                                      if months[order.created_at.month - 1] ==
                                      mon])
            month_totals["total_orders"] = month_orders_total
            month_totals["total_value"] = month_orders_value
            monthly_totals[mon] = month_totals

        return jsonify({"monthly_totals": monthly_totals}), 200
    else:
        abort(404)

