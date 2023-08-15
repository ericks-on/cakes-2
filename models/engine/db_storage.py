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
from models.expenditure import Expenditure
from models.item import Item
from models.input import Input
from models.order import Order
from models.product import Product
from models.product_sales import ProductSales
from models.chat import Chat
from models.message import Message
from dotenv import load_dotenv
from passlib.hash import bcrypt


load_dotenv()
tables = [User.__table__, Product.__table__, Transaction.__table__,
          Expenditure.__table__, Item.__table__, Input.__table__,
          Order.__table__, ProductSales.__table__, Cash.__table__,
          Mpesa.__table__, Chat.__table__, Message.__table__]


class DBStorage:
    """This is the db storage model"""
    __session = None
    __engine = None

    def __init__(self):
        """initialization"""
        user = os.environ.get('KIMUKA_SQL_USER')
        password = os.environ.get('KIMUKA_SQL_PWD')
        host = os.environ.get('KIMUKA_SQL_HOST')
        db = os.environ.get('KIMUKA_SQL_DB')
        port = 3306
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format
                                      (user, password, host, port, db),
                                      pool_pre_ping=True)

    def add(self, obj):
        """adding new object to session"""
        # try:
        #     password = obj.password
        #     obj.password = bcrypt.hash(password)
        # except AttributeError:
        #     pass
        session = self.__session()
        session.add(obj)

    def delete(self, obj):
        """deleting object from db"""
        session = self.__session()
        session.delete(obj)

    def reload(self):
        """creating scoped session and all tables"""
        Base.metadata.create_all(self.__engine, tables=tables)
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory)

    def all(self, cls):
        """Getting all objects on a table specified"""
        session = self.__session()
        objects = session.query(cls).all()
        return objects

    def get(self, cls, obj_id):
        """used to get object by id"""
        session = self.__session()
        obj = session.query(cls).filter_by(id=obj_id).first()
        return obj

    def get_user(self, username):
        """gets user if the username exists"""
        session = self.__session()
        user = session.query(User).filter_by(username=username).first()
        return user
    
    def get_product(self, name):
        """gets product if the name exists"""
        session = self.__session()
        product = session.query(Product).filter_by(name=name).first()
        return product

    def count(self, cls):
        """counts all items on the table based on cls"""
        return self.__session.query(cls).count()

    def save(self):
        """saves all the changes to the storage"""
        session = self.__session()
        session.commit()

    def close(self):
        """removes current session"""
        self.__session.remove()

