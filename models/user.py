#!/usr/bin/python3
"""This contains the user model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer


class User(Basemodel, Base):
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone = Column(String(60), nullable=False)
    user_type = Column(String(60), default="normal")
