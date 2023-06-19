#!/usr/bin/python3
"""Contains the Mpesa model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from models.transaction import Transaction
from sqlalchemy.orm import relationship


class Mpesa(Basemodel, Base):
    """The Mpesa model"""
    __tablename__ = "mpesa"
    transaction_code = Column(String(60), nullable=False, unique=True)
    amount = Column(Integer, nullable=False)
    transaction_id = Column(String(60), nullable=False,
                            ForeignKey('transactions.id'))
    transactions = relationship(Transaction, back_populates='mpesa')

    __table_args__ = (
            CheckConstraint('Amount >= 0', name='positive_constraint'), )
