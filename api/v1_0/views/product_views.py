#!/usr/bin/python3
"""Contains views for products"""
from flask import Blueprint, jsonify, abort, request
from flasgger.utils import swag_from
from models import storage
from models.product import Product
from models.user import User


products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/', methods=['GET'])
@swag_from('documentation/product/all_products.yml')
def all_products():
    """To obtain all products"""
    products = [product.to_dict() for product in storage.all(Product)]
    return jsonify({"products": products}), 200

@products_bp.route('/', methods=['POST'])
@swag_from('documentation/product/add_product.yml')
def add_product():
    """ Adds new product"""
    # filter name and price
    if not request.json():
        abort(400, "Not a JSON")
    if not request.json().get("name"):
        abort(400, "Missing name")
    if not request.json().get("price"):
        abort(400, "Missing price")
    name = request.json().get("name")
    price = request.json().get("price")
    new_product = Product(name=name, price=price)
    storage.add(new_product)
    storage.save()
    return jsonify(new_product.to_dict()), 200

@products_bp.route('/<product_id>', methods=['GET'])
@swag_from('documentation/product/get_product_by_id.yml')
def get_product_by_id(product_id):
    """Getting product by id from url"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    return jsonify(product.to_dict()), 200

@products_bp.route('/<product_id>', methods=['DELETE'])
@swag_from('documentation/product/delete_product_by_id.yml')
def delete_product_by_id(product_id):
    """Deleting product by id from url"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    storage.delete(product)
    storage.save()
    return jsonify({}), 200

@products_bp.route('/<product_id>', methods=['PUT'])
@swag_from('documentation/product/update_product_by_id.yml')
def update_product_by_id(product_id):
    """Updating product by id from url"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    if not request.json():
        abort(400, "Not a JSON")
    if not request.json().get("name"):
        abort(400, "Missing name")
    if not request.json().get("price"):
        abort(400, "Missing price")
    product.name = request.json().get("name")
    product.price = request.json().get("price")
    storage.save()
    return jsonify(product.to_dict()), 200

@products_bp.route('/sales', methods=['GET'])
@swag_from('documentation/product/get_sales.yml')
def get_sales():
    """Getting sales"""
    products = storage.all(Product)
    if not products:
        abort(404)
    sales = {}
    for product in products:
        sales[product.name] = product.sales
    return jsonify(sales), 200
