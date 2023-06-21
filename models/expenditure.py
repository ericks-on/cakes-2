#!/usr/bin/python3
"""Contains the Expenditure model"""
from models.base_model import Basemodel, Base
from flask import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.item import Item


class Expenditure(Basemodel, Base):
    """The Expenditure model"""
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    description = Column(String(1024), nullable=False)
    amount = Column(Integer, nullable=False)

    items = relationship(Item, backref='expenditure', cascade='all, delete')
