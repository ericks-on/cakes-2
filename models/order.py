#!/usr/bin/python3
"""Contains the Order model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey


class Order(Basemodel, Base):
    """the Order model"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    status = Column(String(60), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_value = Column(Integer, nullable=False)
    uom = Column(String(60), nullable=False, default='packets')

    __table_args__ = (
            CheckConstraint('quantity >= 0', name='positive_quantity'),
            CheckConstraint('order_value >= 0', name='positive_value')
            )
