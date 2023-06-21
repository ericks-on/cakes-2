#!/usr/bin/python3
"""Contains model for inputs"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer


class Input(Basemodel, Base):
    """The model for inputs"""
    __tablename__ = 'inputs'
    name = Column(String(60), nullable-False)
    price = Column(Integer, nullable=False)

    __table_arg__ = (
            CheckConstraint('price >= 0', name='positive_constraint'),
            )
