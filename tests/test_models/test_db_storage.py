#!/usr/bin/python3
"""Contains tests for the db storage"""
from models.engine.db_storage import DBStorage
from models.cash import Cash
import unittest


class StorageTestCase(unittest.TestCase):
    """Testing the db storage"""
    def test_add_and_save(self):
        """testing the add method"""
        obj = Cash(Amount=1000)
        storage = DBStorage()
        storage.reload()
        storage.add(obj)
        storage.save()
