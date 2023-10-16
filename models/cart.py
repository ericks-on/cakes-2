#!/usr/bin/python3
"""The cart"""
from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import Basemodel, Base


class Cart(Basemodel, Base):
    """The cart"""
    __tablename__ = 'cart'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)