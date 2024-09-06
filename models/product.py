#!/usr/bin/python3
"""Contains the Product model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from models.product_sales import ProductSales
from models.order import Order


class Product(Basemodel, Base):
    """The model for products"""
    __tablename__ = 'products'
    name = Column(String(60), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    image = Column(String(60), nullable=False)

    sales = relationship(ProductSales, backref='products')

    __table_args__ = (
            CheckConstraint('price >= 0', name='positive_pd_price'),
    )