#!/usr/bin/python3
"""Contains model for inputs"""
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey
from models.base_model import Basemodel, Base


class Inventory(Basemodel, Base):
    """The model for inputs"""
    __tablename__ = 'inventory'
    name = Column(String(60), nullable=False)
    quantity = Column(Integer, nullable=False)
    input_id = Column(String(60), ForeignKey('inputs.id'),
                      nullable=False)

    __table_arg__ = (
            CheckConstraint('price >= 0', name='positive_price'),
            CheckConstraint('quantity >= 0', name='positive_quantity')
            )
