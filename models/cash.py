#!/usr/bin/python3
"""This module contains the Cash model"""
from models.base_model import Basemodel, base
from sqlalchemy import Column, String, Integer, CheckConstraint


class Cash(Basemodel, Base):
    """The cash model"""
    __tablename__ = "cash"
    Transaction_type = Column(String(60), nullable=False, default="cash")
    Amount = Column(Integer, nullable=False)
    

     __table_args__ = (CheckConstraint('Amount >= 0',
                                       name='positive_constraint'),
                                       )
