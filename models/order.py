#!/usr/bin/python3
"""Contains the Order model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from models.product_sales import ProductSales


class Order(Basemodel, Base):
    """the Order model"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    status = Column(String(60), nullable=False, default='pending')
    order_value = Column(Integer, nullable=False)

    products = relationship(ProductSales, backref='order')

    __table_args__ = (
            CheckConstraint('order_value >= 0', name='positive_value'),
            )
