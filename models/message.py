#!/usr/bin/python3
"""Contains the class definition of a Message."""
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_model import Basemodel, Base


class Message(BaseModel, Base):
    """This is the Message model"""
    __tablename__ = 'messages'
    chat_id = Column(String(60), ForeignKey('chats.id'), nullable=False)
    content = Column(String(4096), nullable=False)