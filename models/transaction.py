#!/usr/bin/python3
"""Contains the Transaction model"""
from models.base_model import Basemodel, Base
from sqlalchemy import String, Integer, Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from models.cash import Cash
from models.mpesa import Mpesa


class Transaction(Basemodel, Base):
    """Defining the transactions table a union of cash and mpesa"""
    __tablename__ = "transactions"
    transaction_type = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    cash = relationship(Cash, backref='transactions', cascade='all, delete')
    mpesa = relationship(Mpesa, backref='transactions', cascade='all, delete')

    __table_args__ = (
            CheckConstraint('amount >= 0', name='positive_amount'),
            )
