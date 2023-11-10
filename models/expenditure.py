#!/usr/bin/python3
"""Contains the Expenditure model"""
from sqlalchemy import Column, String, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from models.inventory import Inventory
from models.base_model import Basemodel, Base


class Expenditure(Basemodel, Base):
    """The Expenditure model"""
    __tablename__ = 'expenditures'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    description = Column(String(1024), nullable=False)
    amount = Column(Integer, nullable=False)

    items = relationship(Inventory, backref='expenditure', cascade='all, delete')
    __table_args__ = (
            CheckConstraint('amount >= 0', name='positive_expenditure_amt'),
            )
