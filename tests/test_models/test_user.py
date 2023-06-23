#!/usr/bin/python3
"""testing The user model"""
from models.user import User
import unittest
from models.base_model import Basemodel


class TestUser(unittest.TestCase):
    """Testing the user model"""
    def test_instance_of_basemodel(self):
        """testing instance of basemodel"""
        my_user = User()
        self.assertIsInstance(my_user, Basemodel)


if __name__ == "__main__":
    unittest.main()
