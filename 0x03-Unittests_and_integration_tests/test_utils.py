#!/usr/bin/env python3

"""This module provides utilities for accessing nested mappings safely."""

import unittest
from client import *
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    """MyClass stores and manipulates some data."""
    @parameterized.expand(
            [
                ({"a": 1}, ("a",), 1, int),
                ({"a": {"b": 2}}, ("a",), {"b":2}, dict),
                ({"a": {"b": 2}}, ("a", "b"), 2, int)   
             ]
    )
    def test_acccess_int_and_str(self, nested_map, path,  expected):
        """Return the sum of two integers x and y."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result,  expected)

        # self.assertIsInstance(result, expeted_type)



if __name__== "__main__":
    unittest.main()

