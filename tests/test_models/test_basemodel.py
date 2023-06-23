#!/usr/bin/python3
"""Testing the base model"""
import unittest
from models.base_model import Basemodel


class BasemodelTestCase(unittest.TestCase):
    """Testing the base model"""
    def test_initialization(self):
        """test if initialization is successful"""
        test_instance = Basemodel()
        self.assertIsNotNone(test_instance.id)
        self.assertIsNotNone(test_instance.created_at)
        self.assertIsNotNone(test_instance.updated_at)
