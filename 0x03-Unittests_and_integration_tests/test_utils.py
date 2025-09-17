#!/usr/bin/env python3
"""
This module provides unit tests for the access_nested_map function.
"""

from unittest import TestCase, main
from parameterized import parameterized
from client import access_nested_map
from unittest.mock import patch
from utils import get_json


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


if __name__ == "__main__":
    main()
