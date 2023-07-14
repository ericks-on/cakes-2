#!/usr/bin/python3
"""Flask appp to manage web pages"""
from flask import make_response
from flask_jwt_extended import jwt_required, JWTManager
import requests
import os
from datetime import datetime
import calendar
from flask import Flask, render_template, request, redirect, url_for, jsonify
from collections import OrderedDict


app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('KIMUKA_API_SEC_KEY')
host = os.environ.get('KIMUKA_API_HOST')
port = os.environ.get('KIMUKA_API_PORT')


@app.route('/')
def index():
    """This is the route for landing page"""
    return render_template('index.html', urlFor=url_for)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Handles login"""
    if request.method == 'GET':
        return render_template('index.html', urlFor=url_for)
    else:
        url = f"http://{host}:{port}/api/v1_0/login"
        payload = {}
        payload["username"] = request.form["username"]
        payload["password"] = request.form["password"]
        headers = {"Content-Type": "application/json"}
        api_response = requests.post(url=url, json=payload,
                                     headers=headers, timeout=5)
        response_obj = api_response.json()
        if api_response.status_code == 200:
            response = make_response(redirect(url_for('user_page')))
            response.headers["Authorization"] = "Bearer " + response_obj["access_token"]
            return response
        elif api_response.status_code == 401:
            return redirect(url_for('index'))
        
@app.route("/user", methods=['GET'])
@jwt_required()
def user_page():
    """the user page"""
    return render_template('user.html', urlFor=url_for)

@app.route("/order", methods=['GET'])
def order_page():
    """the order page"""
    month = datetime.now().month
    month_str = calendar.month_name[month]
    year = datetime.now().year

    # get orders history
    orders_url = f"http://{host}:{port}/api/v1_0/orders"
    orders_response = requests.get(url=orders_url, timeout=5).json()
    orders = orders_response["orders"]
    order_history = orders[0:10]

    # get products sales for the month
    products_url = f"http://{host}:{port}/api/v1_0/products/sales/total/{year}/{month}"
    products_response = requests.get(url=products_url, timeout=5).json()
    products_sales = products_response["sales"]

    # get sales for previous month so as to compare
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_products_url = f"http://{host}:{port}/api/v1_0/products/sales/total/{prev_year}/{prev_month}"
    prev_products_response = requests.get(url=prev_products_url, timeout=5).json()
    prev_products_sales = prev_products_response["sales"]

    # comparing sales
    sales_comparison = {}
    for product, sales in products_sales.items():
        if product in prev_products_sales:
            prev_sales = prev_products_sales[product]
            current_sales = sales
            if prev_sales == 0:
                if current_sales == 0:
                    sales_comparison[product] = {}
                    sales_comparison[product]["change"] = "same"
                    sales_comparison[product]["percent"] = 0
                else:
                    sales_comparison[product] = {}
                    sales_comparison[product]["change"] = "up"
                    sales_comparison[product]["percent"] = 1
            elif prev_sales > 0:
                if prev_sales > current_sales:
                    sales_comparison[product] = {}
                    sales_comparison[product]["change"] = "down"
                    diff = prev_sales - current_sales
                    sales_comparison[product]["percent"] = diff / prev_sales
                elif prev_sales < current_sales:
                    sales_comparison[product] = {}
                    sales_comparison[product]["change"] = "up"
                    diff = current_sales - prev_sales
                    sales_comparison[product]["percent"] = diff / prev_sales
                else:
                    sales_comparison[product] = {}
                    sales_comparison[product]["change"] = "same"
                    sales_comparison[product]["percent"] = 0
        else:
            sales_comparison[product] = {}
            sales_comparison[product]["change"] = "up"
            sales_comparison[product]["percent"] = 1

    return render_template('orders.html', urlFor=url_for,
                           orders=orders, order_history=order_history,
                            products_sales=products_sales, month=month_str,
                            year=year, sales_comparison=sales_comparison
                           )

@app.route("/sales", methods=['GET'])
def get_sales():
    """get sales for popup"""
    year = datetime.now().year
    month = datetime.now().month
    url = f"http://{host}:{port}/api/v1_0/products/sales/total/{year}"
    api_response = requests.get(url=url, timeout=5).json()
    sales = api_response["monthly_sales"]
    current_sales = OrderedDict()
    months = calendar.month_name[1:month+1]
    for key, value in sales.items():
        curr_sales = []
        for mon in months:
            curr_sales.append(value[mon])
        current_sales[key] = curr_sales
    return jsonify({"monthly_sales": current_sales, "year": year})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
