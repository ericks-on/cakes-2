#!/usr/bin/python3
"""Contains the Mpesa model"""
from modesl.base_model import Basemodel, Base
from sqlalchemy import Column, Integer, String, CheckConstraint


class Mpesa(Basemodel, Base):
    """The Mpesa model"""
    __tablename__ = "mpesa"
    transaction_code = Column(String(60), nullable=False)
    Amount = Column(Integer, nullable=False)
    transaction_type = Column(String(60), nullable=False, default="M-pesa")

    __table_args__ = (CheckConstraint('Amount >= 0',
                                      name='positive_constraint'),
                                      )
