#!/usr/bin/python3
"""testing the other models"""
from models.base_model import Basemodel
from models.transaction import Transaction
from models.cash import Cash
from models import storage
import unittest


class CashTestCase(unittest.TestCase):
    """testing the cash model"""
    def test_instance_of_basemodel(self):
        """test if its an instance of base model"""
        tr = Transaction(amount=200)
        obj = Cash(amount=100, transaction_id=tr.id)
        self.assertIsInstance(obj, Basemodel)
        self.assertIsInstance(obj, Cash)


if __name__ == "__main__":
    unittest.main()
