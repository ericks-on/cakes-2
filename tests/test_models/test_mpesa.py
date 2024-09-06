#!/usr/bin/python3
"""testing the mpesa model"""
from models.base_model import Basemodel
from models.mpesa import Mpesa
from models.transaction import Transaction
from models import storage
import unittest


class ModelsTestCase(unittest.TestCase):
    """testing the mpesa model"""
    def test_instance_of_base_model(self):
        """testing if it is an instance of base model"""
        tr = Transaction(amount=200)
        obj = Mpesa(amount=200, transaction_type=tr.id)
        self.assertIsInstance(obj, Basemodel)
        self.assertIsInstance(obj, Mpesa)


if __name__ == "__main__":
    unittest.main()
