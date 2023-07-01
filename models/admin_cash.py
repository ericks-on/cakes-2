#!/usr/bin/python3
"""This module contains the Cash model for Admin"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Cash(Basemodel, Base):
    """The cash model"""
    __tablename__ = "admin_cash"
    expenditure_id = Column(String(60), ForeignKey('expenditures.id'),
                            nullable=False)
    amount = Column(Integer, nullable=False)

    __table_args__ = (
            CheckConstraint('amount >= 0', name='positive_acash'), )
