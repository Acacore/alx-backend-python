#!/usr/bin/env python3
"""
This module provides unit tests for the access_nested_map function.
"""

from unittest import TestCase, main
from parameterized import parameterized
from client import access_nested_map
from unittest.mock import patch
from utils import get_json, memoize



class TestAccessNestedMap(TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1, int),
        ({"a": {"b": 2}}, ("a",), {"b": 2}, dict),
        ({"a": {"b": 2}}, ("a", "b"), 2, int),
    ])
    def test_access_nested_map(self, nested_map, path, expected, expected_type):
        """Test access_nested_map returns correct value and type."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        self.assertIsInstance(access_nested_map(nested_map, path), expected_type)


    @parameterized.expand([
        ({},("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises a KeyError for missing keys."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)



class TestGetJson(TestCase):
    """Unit tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        #configure mock
        mock_get.return_value.json.return_value = test_payload
        
        #call function
        result = get_json(test_url)
        
        # Assertions
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(TestCase):

    """ TestCase for the memoize decorator. """
    
    def test_memoize(self):
        """
        Test that a memoized property calls the original method only once.
        
        - Creates a TestClass with a method a_method and a memoized property a_property.
        - Patches a_method to monitor calls.
        - Calls a_property twice.
        - Asserts that the result is correct and a_method was called exactly once.
        """
        class TestClass:
            """Test class with a method and a memoized property."""

            def a_method(self):
                """Return a value for testing memoization."""
                return 42

            @memoize
            def a_property(self):
                """Return the value of a_method, memoized."""
                return self.a_method()
            
        obj = TestClass()

        with patch.object(obj, 'a_method') as mock_method:
            mock_method.return_value = 42
            

            # Call the property twice
            result1 = obj.a_property
            result2 = obj.a_property


            # Assert the property returns expected value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method ws called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    main()
