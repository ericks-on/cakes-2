#!/usr/bin/python3
"""Contains the class definition of a Chat."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Basemodel, Base
from models.message import Message


class Chat(Basemodel, Base):
    """This is the Chat model"""
    __tablename__ = 'chats'
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    recepient_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    subject = Column(String(128), nullable=False)

    messages = relationship(Message, backref='chat', cascade='all, delete')