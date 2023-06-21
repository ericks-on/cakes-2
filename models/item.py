#!/usr/bin/python3
"""This contains the Item model"""
from flask import Column, String, Integer, FoeignKey
from models.base_model import Basemodel, Base


class Item(Basemodel, Base):
    """The item model"""
    __tablename__ = 'items'
    input_id = Column(String(60), ForeignKey('inputs.id'), nullable=False)
    expenditure_id = Column(String(60), ForeignKey('expenditures.id'),
                            nullable=False)
