import unittest
from client import *
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand(
            [
                ({"a": 1}, ("a",), 1, int),
                ({"a": {"b": 2}}, ("a",), {"b":2}, dict),
                ({"a": {"b": 2}}, ("a", "b"), 2, int)   
             ]
    )
    def test_acccess_int_and_str(self, nested_map, path,  expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result,  expected)

        # self.assertIsInstance(result, expeted_type)



if __name__== "__main__":
    unittest.main()

