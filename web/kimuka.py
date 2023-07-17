#!/usr/bin/python3
"""Flask appp to manage web pages"""
import os
import calendar
from datetime import datetime
import requests
from collections import OrderedDict
from flask import make_response
from flask_jwt_extended import jwt_required, JWTManager
from flask_jwt_extended import  set_access_cookies, unset_jwt_cookies
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('KIMUKA_API_SEC_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config["JWT_COOKIE_SECURE"] = True
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
        url = f"http://{host}:{port}/api/v1_0/token/auth"
        payload = {}
        payload["username"] = request.form["username"]
        payload["password"] = request.form["password"]
        api_response = requests.post(url=url, json=payload, timeout=5)
        response_obj = api_response.json()
        if api_response.status_code == 200:
            response = make_response(redirect(url_for('order_page')))
            # headers = {'Content-Type': 'text/html',
            #            'Authorization': f"Bearer {response_obj['access_token']}"
            # }
            # response.headers = headers
            set_access_cookies(response, response_obj['access_token'])
            return response
        elif api_response.status_code == 401:
            return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Handles logout"""
    response = jsonify({'logout': True})
    response = make_response(response)
    unset_jwt_cookies(response)
    return response

@app.route("/user", methods=['GET'])
@jwt_required()
def user_page():
    """the user page"""
    return render_template('user.html', urlFor=url_for)

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

    # =================================get orders history================================
    orders_url = f"http://{host}:{port}/api/v1_0/orders"
    orders_response = requests.get(url=orders_url, headers=headers,
                                   timeout=5).json()
    orders = orders_response["orders"]
    order_history = orders[0:10]

    # =======================get products sales for the month============================
    products_url = f"""http://{host}:{port}/api/v1_0/products/sales/total/{year}/{month}"""
    products_response = requests.get(url=products_url, headers=headers,
                                     timeout=5).json()
    products_sales = products_response["sales"]

    # =============================get sales for previous month so as to compare============
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_products_url = f"http://{host}:{port}/api/v1_0/products/sales/total/{prev_year}/{prev_month}"
    prev_products_response = requests.get(url=prev_products_url, headers=headers,
                                          timeout=5).json()
    prev_products_sales = prev_products_response["sales"]

    # ================================comparing sales btn current and previous month===========================
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
    sales_url = f"http://{host}:{port}/api/v1_0/products/sales/total"
    sales_response = requests.get(url=sales_url, headers=headers,
                                  timeout=5).json()
    sales_totals = sales_response["sales"]
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
    app.run(host='0.0.0.0', port=5000, debug=True)
