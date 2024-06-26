#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import json
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock

import models
import pep8
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine import db_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(
            len(db_storage.__doc__) >= 1, "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(
            len(DBStorage.__doc__) >= 1, "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]))

    def test_get_existing_object(self):
        """Mocking the query result for testing"""
        query_result = MagicMock()
        self.storage._DBStorage__session.query().filter(
        ).first.return_value = query_result
        """Testing get() method for an existing object"""
        result = self.storage.get(User, 'test_id')
        self.assertEqual(result, query_result)

    def test_get_nonexistent_object(self):
        # Mocking the query result for testing
        self.storage._DBStorage__session.query().filter(
        ).first.return_value = None

        # Testing get() method for a non-existent object
        result = self.storage.get(User, 'nonexistent_id')
        self.assertIsNone(result)

    def test_count_all_objects(self):
        # Mocking the query result for testing
        self.storage._DBStorage__session.query().count.return_value = 2

        # Testing count() method for all objects
        result = self.storage.count()
        self.assertEqual(result, 2)

    def test_count_objects_by_class(self):
        # Mocking the query result for testing
        self.storage._DBStorage__session.query().filter(
        ).count.return_value = 1

        # Testing count() method for objects of a specific class
        result = self.storage.count(User)
        self.assertEqual(result, 1)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_existing_object(self):
        # Mocking objects for testing
        test_obj = MagicMock()
        test_obj.id = 'test_id'
        test_obj.__class__.__name__ = 'TestClass'

        # Adding the mock object to the storage
        self.storage._FileStorage__objects['TestClass.test_id'] = test_obj

        # Testing get() method
        result = self.storage.get(User, 'test_id')
        self.assertEqual(result, test_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent_object(self):
        # Testing get() method for a non-existent object
        result = self.storage.get(User, 'nonexistent_id')
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        # Mocking objects for testing
        self.storage._FileStorage__objects = {
            'TestClass1.test_id': MagicMock(),
            'TestClass2.test_id': MagicMock()
        }

        # Testing count() method for all objects
        result = self.storage.count()
        self.assertEqual(result, 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_objects_by_class(self):
        # Mocking objects for testing
        self.storage._FileStorage__objects = {
            'TestClass1.test_id': MagicMock(),
            'TestClass2.test_id': MagicMock()
        }

        # Testing count() method for objects of a specific class
        result = self.storage.count(User)
        self.assertEqual(result, 1)
