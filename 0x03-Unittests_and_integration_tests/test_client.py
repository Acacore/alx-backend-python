#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient and related utilities.
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient, access_nested_map
from utils import get_json, memoize
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function."""

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
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        """Test access_nested_map raises KeyError for missing keys."""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns correct payload."""
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """TestCase for the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized property calls the original method only once."""

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

        with patch.object(obj, "a_method") as mock_method:
            mock_method.return_value = 42

            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"org": "google"}),
        ("abc", {"org": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the expected payload."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns expected result."""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/test/repos")
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos."""
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_payload

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly checks repo licenses."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get at class level."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repository names without license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repository names filtered by license='apache-2.0'."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
