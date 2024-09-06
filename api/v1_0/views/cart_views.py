#!usr/bin/python3
"""CRUD operations for the cart"""
from flask import Blueprint, jsonify, abort, request
from flasgger.utils import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.cart import Cart
from models.product import Product


cart_bp = Blueprint('cart_bp', __name__, url_prefix='/cart')


@cart_bp.route('/', methods=['GET'])
@swag_from('documentation/cart/all_cart.yml')
@jwt_required()
def get_cart():
    """Getting all items in the cart"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(403)
    cart_items = [item for item in storage.all(Cart)
                  if item.user_id == user.id]
    cart = [{"product_id": item.product_id,
             "quantity": item.quantity,
             "name": storage.get(Product, item.product_id).name,
             "price": storage.get(Product, item.product_id).price,
             "image": storage.get(Product, item.product_id).image
             } for item in cart_items]
    return jsonify({"cart": cart}), 200
    
@cart_bp.route('/', methods=['POST'])
@swag_from('documentation/cart/add_cart.yml')
@jwt_required()
def add_cart():
    """Adding new item to cart"""
    product_id = request.get_json().get('product_id')
    quantity = request.get_json().get('quantity')
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(403)
    product = storage.get(Product, product_id)
    if not product:
        abort(400)
    if not product_id or not quantity:
        abort(400)
    
    new_item = Cart(product_id=product_id, quantity=quantity, user_id=user.id)
    storage.add(new_item)
    storage.save()
    return jsonify({product.name: new_item.to_dict()}), 201

@cart_bp.route('/<product_id>', methods=['DELETE'])
@swag_from('documentation/cart/delete_cart.yml')
@jwt_required()
def del_cart(product_id):
    """Deleting item from cart"""
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(403)
    product_ids = [item.product_id for item in storage.all(Cart)
                if item.user_id == user.id]
    cart = [item for item in storage.all(Cart)
            if item.user_id == user.id]
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    if product_id not in product_ids:
        abort(404)
    for item in cart:
        if item.product_id == product_id:
            storage.delete(item)
            storage.save()
            return jsonify({product.name: {}}), 200

@cart_bp.route('/<product_id>', methods=['PUT'])
@swag_from('documentation/cart/update_cart.yml')
@jwt_required()
def update_cart(product_id):
    """Updating cart item quantity"""
    quantity = request.get_json().get('quantity')
    user = storage.get_user(get_jwt_identity())
    if not user:
        abort(403)
    cart = [item for item in storage.all(Cart)
            if item.user_id == user.id]
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    if not quantity:
        abort(400)
    for item in cart:
        if item.product_id == product_id:
            item.quantity = quantity
            storage.save()
            return jsonify({product.name: item.to_dict()}), 200
    abort(404)