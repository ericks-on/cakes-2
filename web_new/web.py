#!/usr/bin/python3
"""Managing the web pages"""
import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def login():
    """Login page"""
    return render_template('admin.html')


if __name__ == '__main__':
    host = os.environ.get('WEB_HOST')
    port = os.environ.get('WEB_PORT')
    app.run(host=host, port=port, debug=True)