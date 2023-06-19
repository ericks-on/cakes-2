#!/usr/bin/python3
"""This module contains the Cash model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from models.transaction import Transaction

class Cash(Basemodel, Base):
    """The cash model"""
    __tablename__ = "cash"
    transaction_id = Column(String(60), nullable=False,
                            ForeignKey('transactions.id'))
    amount = Column(Integer, nullable=False)
    transactions = relationship(Transaction, back_populates='cash')
    

    __table_args__ = (
            CheckConstraint('Amount >= 0', name='positive_constraint'), )
