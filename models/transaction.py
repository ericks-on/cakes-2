#!/usr/bin/python3
"""This contains the transactions model"""
from models.base_model import Basemodel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import union_all
# import session


class Transaction(Basemodel, Base):
    """The transaction model"""
    __table__ = union_all(session.query(Cash.id.label('Transaction_id'),
                                        cash.Transaction_type, Amount),
                          session.query(mpesa.id.label('Transaction_id'),
                                        mpesa.Transction_type,
                                        Amount)).alias('transactions')
                              
