#!/usr/bin/python3
"""This contains the ProductSales model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class ProductSales(BaseModel, Base):
    """The model for product sales"""
    __tablename__ = 'product_sales'

    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    uom = Column(String(60), nullable=False, default='packets')
    sales_value = Column(Integer, nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)

    __table_args__ = (
            CheckConstraint('quantity >= 0', name='positive_quantity'),
            CheckConstraint('sales_value >= 0', name='positive_value')
            )

