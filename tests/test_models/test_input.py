#!/usr/bin/python3
"""Contains tests for the Input model"""
from models.base_model import Basemodel
from models.input import Input
from models import storage
import unittest
import sqlalchemy


class InputTestCase(unittest.TestCase):
    """testing the Input model"""
    def test_instance_of_basemodel(self):
        """test if its an instance of base model"""
        obj = Input(name='bb')
        self.assertIsInstance(obj, Basemodel)
        self.assertIsInstance(obj, Input)

    def tearDown(self):
        """cleanup"""
        storage.close()

    def test_null_name_column(self):
        """Test when name column is null"""
        obj = Input(price=100, quantity=1, uom='pieces')
        with self.assertRaises(sqlalchemy.exc.OperationalError) as cm:
            storage.add(obj)
            storage.save()

        error_message = str(cm.exception)
        self.assertIn("Column 'name' cannot be null", error_message)
    
    def test_null_price_column(self):
        """Test when price column is null"""
        obj = Input(name="some name", quantity=1, uom='pieces')
        with self.assertRaises(sqlalchemy.exc.OperationalError) as cm:
            storage.add(obj)
            storage.save()

        error_message = str(cm.exception)
        self.assertIn("Column 'price' cannot be null", error_message)

    def test_null_quantity_column(self):
        """Test when quantity column is null"""
        obj = Input(price=100, name="some name", uom='pieces')
        with self.assertRaises(sqlalchemy.exc.OperationalError) as cm:
            storage.add(obj)
            storage.save()

        error_message = str(cm.exception)
        self.assertIn("Column 'quantity' cannot be null", error_message)

    def test_null_uom_column(self):
        """Test when uom column is null"""
        obj = Input(price=100, quantity=1, name='pieces')
        with self.assertRaises(sqlalchemy.exc.OperationalError) as cm:
            storage.add(obj)
            storage.save()

        error_message = str(cm.exception)
        self.assertIn("Column 'uom' cannot be null", error_message)



if __name__ == "__main__":
    unittest.main()
