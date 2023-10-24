#!/usr/bin/python3
"""This contains the user model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer
from models.transaction import Transaction
from sqlalchemy.orm import relationship
from models.order import Order
from models.expenditure import Expenditure
from models.chat import Chat
from models.message import Message
from models.cart import Cart


class User(Basemodel, Base):
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(60), nullable=False)
    user_type = Column(String(60), default="normal")
    username = Column(String(60), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    transactions = relationship(Transaction, backref='users')
    expenditures = relationship(Expenditure, backref='user')
    orders = relationship(Order, backref='orders', cascade='all, delete')
    send_chats = relationship(Chat, backref='sender',
                              foreign_keys='Chat.sender_id')
    received_chats = relationship(Chat, backref='recepient',
                                  foreign_keys='Chat.recepient_id')
    messages = relationship(Message, backref='sender')
    cart = relationship(Cart, backref='user', cascade='all, delete')
