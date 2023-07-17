#!/usr/bin/python3
"""Contains views for products"""
from flask import Blueprint, jsonify, abort, request
from flasgger.utils import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.product import Product
from models.user import User
import calendar


products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/', methods=['GET'])
@swag_from('documentation/product/all_products.yml')
@jwt_required()
def all_products():
    """To obtain all products"""
    products = [product.to_dict() for product in storage.all(Product)]
    return jsonify({"products": products}), 200

@products_bp.route('/', methods=['POST'])
@swag_from('documentation/product/add_product.yml')
@jwt_required()
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
    return jsonify(new_product.to_dict()), 201

@products_bp.route('/<product_id>', methods=['GET'])
@swag_from('documentation/product/get_product_by_id.yml')
@jwt_required()
def get_product_by_id(product_id):
    """Getting product by id from url"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    return jsonify(product.to_dict()), 200

@products_bp.route('/<product_id>', methods=['DELETE'])
@swag_from('documentation/product/delete_product_by_id.yml')
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def get_sales():
    """Getting sales"""
    products = storage.all(Product)
    if not products:
        abort(404)
    sales = {}
    for product in products:
        sales[product.name] = [sale.to_dict() for sale in product.sales]
    return jsonify({"sales": sales}), 200

@products_bp.route('/sales/date/<year>', methods=['GET'])
@products_bp.route('/sales/date/<year>/<month>', methods=['GET'])
@swag_from('documentation/product/get_sales_by_year_month.yml')
@jwt_required()
def get_sales_by_year_month(year, month=None):
    """Getting sales by year and month"""
    products = storage.all(Product)
    if not products:
        abort(404)
    sales = {}
    for product in products:
        if month:
            sales[product.name] = [sale.to_dict() for sale in product.sales
                                   if sale.created_at.year == int(year)
                                   and sale.created_at.month == int(month)]
        else:
            sales[product.name] = [sale.to_dict() for sale in product.sales
                                   if sale.created_at.year == int(year)]
    return jsonify({"sales": sales}), 200

@products_bp.route('/sales/<product_name>', methods=['GET'])
@swag_from('documentation/product/get_sales_by_name.yml')
@jwt_required()
def get_sales_by_name(product_name):
    """Getting sales by name"""
    product = storage.get_product(product_name)
    if not product:
        abort(404)
    sales = [sale.to_dict() for sale in product.sales]
    return jsonify({product_name: sales}), 200

@products_bp.route('/sales/<product_name>/<year>', methods=['GET'])
@products_bp.route('/sales/<product_name>/<year>/<month>', methods=['GET'])
@swag_from('documentation/product/get_sales_by_name_year_month.yml')
@jwt_required()
def get_sales_by_name_year_month(product_name, year, month=None):
    """Getting sales by name, year and month"""
    product = storage.get_product(product_name)
    if not product:
        abort(404)
    if month:
        sales = [sale.to_dict() for sale in product.sales
                 if sale.created_at.year == int(year)
                 and sale.created_at.month == int(month)]
    else:
        sales = [sale.to_dict() for sale in product.sales
                 if sale.created_at.year == int(year)]
    return jsonify({product_name: sales}), 200

@products_bp.route('/sales/total', methods=['GET'])
@swag_from('documentation/product/get_total_sales.yml')
@jwt_required()
def get_total_sales():
    """Getting total sales"""
    products = storage.all(Product)
    if not products:
        abort(404)
    sales = {}
    for product in products:
        tsales_price = {}
        total_sales = sum([sale.quantity for sale in product.sales])
        tsales_price["total_sales"] = total_sales
        tsales_price["price"] = product.price
        sales[product.name] = tsales_price
    return jsonify({"sales": sales}), 200

@products_bp.route('/sales/total/<year>/<month>', methods=['GET'])
@products_bp.route('/sales/total/<year>', methods=['GET'])
@swag_from('documentation/product/get_total_sales_within_period.yml')
@jwt_required()
def get_total_sales_within_period(year, month=None):
    """Getting total sales"""
    products = storage.all(Product)
    if not products:
        abort(404)

    if month:
        sales = {}
        for product in products:
            total_sales = sum([sale.quantity for sale in product.sales
                            if sale.created_at.year == int(year)
                            and sale.created_at.month == int(month)])
            sales[product.name] = total_sales
        return jsonify({"sales": sales}), 200
    else:
        months = calendar.month_name[1:]
        sales = {}
        for product in products:
            pdt_monthly_sales = {}
            for mon in months:
                total_sales = sum([sale.quantity for sale in product.sales
                                   if sale.created_at.year == int(year)
                                   and sale.created_at.month == 
                                   months.index(mon)+1])
                pdt_monthly_sales[mon] = total_sales
            sales[product.name] = pdt_monthly_sales
        return jsonify({"monthly_sales": sales}), 200