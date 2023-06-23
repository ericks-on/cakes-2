#!/usr/bin/python3
"""This contains the Item model"""
from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import Basemodel, Base


class Item(Basemodel, Base):
    """The item model"""
    __tablename__ = 'items'

    expenditure_id = Column(String(60), ForeignKey('expenditures.id'),
                            nullable=False)
    input_id = Column(String(60), ForeignKey('inputs.id'), nullable=False)
