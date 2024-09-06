#!/usr/bin/python3
"""Contains the Mpesa model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Mpesa(Basemodel, Base):
    """The Mpesa model"""
    __tablename__ = "mpesa"
    TransID = Column(String(60), nullable=False, unique=True)
    TransAmount = Column(Integer, nullable=False)
    MSISDN = Column(String(60), nullable=False)
    FirstName = Column(String(60), nullable=False)
    MiddleName = Column(String(60))
    LastName = Column(String(60), nullable=False)
    transaction_id = Column(String(60), ForeignKey('transactions.id'),
                            nullable=False)

    __table_args__ = (
            CheckConstraint('TransAmount >= 0', name='positive_mpesa'), )
