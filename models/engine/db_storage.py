#!/usr/bin/python3
"""This contains the db storage model"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.user import User
from models.cash import Cash
from models.mpesa import Mpesa
from models.transaction import Transaction


models = {'User': User, 'Transaction': Transaction, 'Cash': Cash,
          'Mpesa': Mpesa}
class DBStorage:
    """This is the db storage model"""
    __session = None
    __engine = None

    def __init__(self):
        """initialization"""
        user = os.environ.get('CAKES_USER')
        password = os.environ.get('CAKES_PWD')
        host = os.envoron.get('CAKES_HOST')
        db = os.environ.get('CAKES_DB')
        port = os.environ.get('CAKES_PORT')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format
                                      (password, user, host, port, db),
                                      pool_pre_ping=True)

    def add(self, obj):
        """adding new object to db"""
        session = self.__session()
        session.add(obj)

    def delete(self, obj):
        """deleting object from db"""
        session = self.__session()
        session.delete(obj)

    def reload(self):
        """creating scoped session and all tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory)

    def count(self, cls):
        """counts all items on the table based on cls"""
        return len(self.__session.query(cls).all())

