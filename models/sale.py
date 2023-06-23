#!/usr/bin/python3
"""Contains the sales model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, ForeignKey, CheckConstraint, Integer


class Sale(Basemodel, Base):
    """Defines how user record a sale"""
    __tablename__ = "sales"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    no_of_cakes = Column(Integer, nullable=False)

    __table_args__ = (
            CheckConstraint('no_of_cakes >= 0', name='positive_constraint'),
            )
