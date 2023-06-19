#!/usr/bin/python3
"""Contains the Transaction model"""
from models.base_model import Basemodel, Base
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models.cash import Cash
from models.mpesa import Mpesa
from models.user import User


class Transaction(Basemodel, Base):
    """Defining the transactions table a union of cash and mpesa"""
    __tablename__ = "transactions"
    transaction_type = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False, ForeignKey('users.id'))
    amount = Column(Integer, nullable=False)
    cash = relationship(Cash, back_populates='transactions',
                        cascade='all, delete')
    mpesa = relationship(Mpesa, back_populates='transactions',
                         cascade='all, delete')
    users = relationship(User, back_populates='transactions')
