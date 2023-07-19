#!/usr/bin/python3
"""Flask appp to manage web pages"""
import os
import calendar
from datetime import datetime
import requests
from collections import OrderedDict
from flask import make_response, abort
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity
from flask_jwt_extended import  set_access_cookies, unset_jwt_cookies
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from web.socket_events import socketio
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
jwt = JWTManager(app)
app.secret_key = os.environ.get('KIMUKA_API_SEC_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('KIMUKA_API_SEC_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
socketio.init_app(app)
# app.config["JWT_COOKIE_SECURE"] = True
host = os.environ.get('KIMUKA_API_HOST')
port = os.environ.get('KIMUKA_API_PORT')


@jwt.expired_token_loader
@jwt.invalid_token_loader
def handle_invalid_token_callback(error):
    """Handles invalid token"""
    return redirect(url_for('index'))

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
        url = f"http://{host}:{port}/api/v1_0/token/auth"
        payload = {}
        payload["username"] = request.form["username"]
        payload["password"] = request.form["password"]
        api_response = requests.post(url=url, json=payload, timeout=5)
        response_obj = api_response.json()
        if api_response.status_code == 200:
            response = make_response(redirect(url_for('message_page')))
            set_access_cookies(response, response_obj['access_token'])
            return response
        elif api_response.status_code == 401:
            return redirect(url_for('index'))

@app.route('/logout')
@jwt_required()
def logout():
    """Handles logout"""
    response = redirect(url_for('index'))
    response = make_response(response)
    unset_jwt_cookies(response)
    return response

@app.route("/messages", methods=['GET'])
@jwt_required()
def message_page():
    """the user page"""
    return render_template('messages.html', urlFor=url_for)

@app.route("/order", methods=['GET'])
@jwt_required()
def order_page():
    """the order page"""
    month = datetime.now().month
    month_str = calendar.month_name[month]
    year = datetime.now().year
    access_token = request.cookies.get('access_token_cookie') 
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {access_token}"
    }
    user_url = f"http://{host}:{port}/api/v1_0/users"
    try:
        user_response = requests.get(url=user_url, headers=headers,
                                        timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")
    try:
        user = user_response["users"]
    except KeyError:
        error = user_response["error"]
        abort(500, error)

    # =================================get orders history================================
    orders_url = f"http://{host}:{port}/api/v1_0/orders"
    try:
        orders_response = requests.get(url=orders_url, headers=headers,
                                       timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")

    try:
        orders = orders_response["orders"]
    except KeyError:
        error = orders_response["error"]
        abort(500, error)
    order_history = orders[0:10]

    # =======================get products sales for the month============================
    if user["user_type"] == "admin":
        products_url = f"http://{host}:{port}/api/v1_0/products/sales/total/{year}/{month}"
    else:
        products_url = f"http://{host}:{port}/api/v1_0/orders/sales/total/{year}/{month}"

    try:
        products_response = requests.get(url=products_url, headers=headers,
                                         timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")
    try:
        products_sales = products_response["sales"]
    except KeyError:
        error = products_response["error"]
        abort(500, error)

    # =============================get sales for previous month so as to compare============
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    if user["user_type"] == "admin":
        prev_sales_url = f"http://{host}:{port}/api/v1_0/products/sales/total/{prev_year}/{prev_month}"
    else:
        prev_sales_url = f"http://{host}:{port}/api/v1_0/orders/sales/total/{prev_year}/{prev_month}"
    try:
        prev_sales_response = requests.get(url=prev_sales_url,
                                           headers=headers,
                                           timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")

    try:
        prev_products_sales = prev_sales_response["sales"]
    except KeyError:
        error = prev_sales_response["error"]
        abort(500, error)

    # ================================comparing sales btn current and previous month===========================
    sales_comparison = {}
    for product, sales in products_sales.items():
        if product in prev_products_sales.keys():
            prev_sales = prev_products_sales[product]["total_sales"]
            current_sales = sales["total_sales"]
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

    # ==================================Calculating AOV===================================
    total_orders = len(orders)
    total_order_value = 0
    for order in orders:
        order_value = int(order["order_value"])
        total_order_value += order_value
    aov = total_order_value / total_orders
    aov_info = {}
    aov_info["total_orders"] = total_orders
    aov_info["total_order_value"] = total_order_value
    aov_info["aov"] = round(aov, 2)

    # ===================================Calculating sales contribution============================
    if user["user_type"] == "admin":
        sales_url = f"http://{host}:{port}/api/v1_0/products/sales/total"
    else:
        sales_url = f"http://{host}:{port}/api/v1_0/orders/sales/total"
    try:
        sales_response = requests.get(url=sales_url, headers=headers,
                                      timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")

    try:
        sales_totals = sales_response["sales"]
    except KeyError:
        error = sales_response["error"]
        abort(500, error)
    all_sales_sum = 0
    all_sales_value = 0
    for product, value in sales_totals.items():
        all_sales_sum += value["total_sales"]
        all_sales_value += value["total_sales"] * value["price"]
    sales_contribution = {}
    for product, sales in sales_totals.items():
        sales_contribution[product] = {}
        sales_contribution[product]["sales"] = sales["total_sales"]
        sales_contribution[product]["percent"] = round((sales["total_sales"] /
                                                        all_sales_sum) * 100, 2)

    most_sales = max([value["total_sales"] for value in sales_totals.values()])
    sales_values_totals = {}
    for product, value in sales_totals.items():
        sales_values_totals[product] = value["total_sales"]
    indices = [index for index, value in
               enumerate(list(sales_values_totals.values()))
               if value == most_sales]
    most_popular = [list(sales_totals.keys())[index] for index in indices]

    return render_template('orders.html', urlFor=url_for,
                           orders=orders, order_history=order_history,
                           products_sales=products_sales, month=month_str,
                           year=year, sales_comparison=sales_comparison,
                           aov_info=aov_info, most_popular=most_popular,
                           sales_contribution=sales_contribution,
                           all_sales_value=all_sales_value
                           )

@app.route("/api/sales", methods=['GET'])
def get_sales():
    """get sales for popup"""
    year = datetime.now().year
    month = datetime.now().month
    access_token = request.cookies.get('access_token_cookie')
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{host}:{port}/api/v1_0/orders/sales/total/{year}"
    try:
        api_response = requests.get(url=url, headers=headers,
                                    timeout=5).json()
    except requests.exceptions.ConnectionError:
        abort(500, "Connection error")

    try:
        sales = api_response["monthly_sales"]
    except KeyError:
        error = api_response["error"]
        abort(500, error)
    current_sales = OrderedDict()
    months = calendar.month_name[1:month+1]
    for key, value in sales.items():
        curr_sales = []
        for mon in months:
            curr_sales.append(value[mon]["total_sales"])
        current_sales[key] = curr_sales
    return jsonify({"monthly_sales": current_sales, "year": year})

@app.route("/api/monthly_aov", methods=['GET'])
def get_monthly_aov():
    """get monthly aov"""
    year = datetime.now().year
    month = datetime.now().month
    access_token = request.cookies.get('access_token_cookie')
    headers = {"Authorization": f"Bearer {access_token}"}
    yearly_orders_url = f"http://{host}:{port}/api/v1_0/orders/totals/{year}"
    yearly_orders_response = requests.get(url=yearly_orders_url, headers=headers,
                                          timeout=5).json()
    monthly_totals = yearly_orders_response["monthly_totals"]
    monthly_orders_totals = []
    monthly_order_values = []
    months = calendar.month_name[1:month+1]
    for mon in months:
        monthly_orders_totals.append(monthly_totals[mon]["total_orders"])
        monthly_order_values.append(monthly_totals[mon]["total_value"])
    monthly_aov = []
    for i in range(len(monthly_orders_totals)):
        if monthly_orders_totals[i] == 0:
            monthly_aov.append(0)
        else:
            monthly_aov.append(monthly_order_values[i] /
                               monthly_orders_totals[i])
    return jsonify({"monthly_aov": monthly_aov, "year": year, "monthly_orders": monthly_orders_totals})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """get all orders"""
    orders_url = f"http://{host}:{port}/api/v1_0/orders"
    orders_response = requests.get(url=orders_url, timeout=5).json()
    orders = orders_response["orders"]
    return jsonify({"orders": orders})



if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, debug=True)
