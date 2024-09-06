from sqlalchemy import Column, Integer, String
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from models.base_model import Base, Basemodel
from models.inventory import Inventory


class Input(Basemodel, Base):
    """The model for inputs"""
    __tablename__ = 'inputs'
    name = Column(String(60), nullable=False)
    cost = Column(Integer, nullable=False)
    inventory = relationship(Inventory, backref='inputs',
                             cascade='all, delete')

    __table_args__ = (
            CheckConstraint('cost >= 0', name='positive_cost'),
            )