#!/usr/bin/python3
"""This contains the user model"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Basemodel, Base
from models.transaction import Transaction
from models.order import Order
from models.cart import Cart


class User(Basemodel, Base):
    """The user model"""
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(60), nullable=False)
    user_type = Column(String(60), default="normal")
    username = Column(String(60), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    transactions = relationship(Transaction, backref='users')
    orders = relationship(Order, backref='orders', cascade='all, delete')
    cart = relationship(Cart, backref='user', cascade='all, delete')
