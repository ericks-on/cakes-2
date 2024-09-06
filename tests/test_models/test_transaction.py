#!/usr/bin/python3
"""testing the other models"""
from models.user import User
from models.base_model import Basemodel
from models.transaction import Transaction
from models import storage
import unittest


class ModelsTestCase(unittest.TestCase):
    """testing the transaction model"""
    def test_instance_of_base_model(self):
        """test if transaction is an instance of basemodel class"""
        obj = Transaction(amount=200)
        self.assertIsInstance(obj, Basemodel)
        self.assertIsInstance(obj, Transaction)


if __name__ == '__main__':
    unittest.main()
