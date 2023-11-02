#!/usr/bin/python3
"""Contains wtf forms"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms.validators import DataRequired


class ProductsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('name', validators=[DataRequired()])