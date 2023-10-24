#!usr/bin/python3
"""CRUD operations for the cart"""
from flask import Blueprint, jsonify, abort, request
from flasgger.utils import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.cart import Cart
from models.product import Product


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/', methods=['GET'])
@swag_from('documentation/cart/all_cart.yml')
@jwt_required()
def get_cart():
    """Getting all items in the cart"""
    user = storage.get_user(get_jwt_identity())
    cart_items = [item for item in storage.all(Cart)
                  if item.user_id == user.id]
    cart = [{"product": storage.get(Product, item.product_id),
             "quantity": item.quantity,
             "total": storage.get(Product, item.product_id).price *
             item.quantity, "id": item.id} for item in cart_items]
    return jsonify({"cart": cart}), 200
    
@cart_bp.route('/', methods=['POST'])
@swag_from('documentation/cart/add_cart.yml')
@jwt_required()
def add_cart():
    """Adding new item to cart"""
    product_id = request.get_json().get('product_id')
    quantity = request.get_json().get('quantity')
    user = storage.get_user(get_jwt_identity())
    if not product_id or not quantity:
        abort(400)
    
    new_item = Cart(product_id=product_id, quantity=quantity, user_id=user.id)
    storage.add(new_item)
    storage.save()
    return jsonify(new_item.to_dict()), 201

@cart_bp.route('/<product_id>', methods=['DELETE'])
@swag_from('documentation/cart/delete_cart.yml')
@jwt_required()
def del_cart(product_id):
    """Deleting item from cart"""
    user = storage.get_user(get_jwt_identity())
    product_ids = [item.product_id for item in storage.all(Cart)
                if item.user_id == user.id]
    cart = [item for item in storage.all(Cart)
            if item.user_id == user.id]
    if product_id not in product_ids:
        abort(404)
    for item in cart:
        if item.product_id == product_id:
            storage.delete(item)
            storage.save()
            return jsonify({}), 200

@cart_bp.route('/<cart_id>', methods=['PUT'])
@swag_from('documentation/cart/update_cart.yml')
@jwt_required()
def update_cart(cart_id):
    """Updating cart item quantity"""
    quantity = request.get_json().get('quantity')
    cart_id = request.get_json().get('cart_id')
    if not quantity or not cart_id:
        abort(400)
    item = storage.get(Cart, cart_id)
    item.quantity = quantity
    storage.save()
    return jsonify(item.to_dict), 200