#!/usr/bin/env python3
Emplement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.

Decorate the method with @parameterized.expand to test the function for following inputs:

nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
For each of these inputs, test with assertEqual that the function returns the expected result.