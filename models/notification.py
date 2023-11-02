#!/usr/bin/python3
"""Contains the notification model"""
from sqlalchemy import String, Column
from models.base_model import Basemodel, Base


class Notification(Basemodel, Base):
    """The Notification model"""
    __tablename__ = "notifications"
    message = Column(String(1024), nullable=False)
    