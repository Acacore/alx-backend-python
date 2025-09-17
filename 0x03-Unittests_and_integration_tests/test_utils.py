#!/usr/bin/env python3
"""
This module provides unit tests for the access_nested_map function.
"""

from unittest import TestCase, main
from parameterized import parameterized
from client import access_nested_map


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


if __name__ == "__main__":
    main()
