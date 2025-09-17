#!/usr/bin/env python3
"""
This module provides unit tests for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestCase for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"org": "google"}),
        ("abc", {"org": "abc"}),
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
        """Test that _public_repos_url returns expected result"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}

        client = GithubOrgClient("test")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/test/repos")
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos"""
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_payload

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")

            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")

    
    # ... (other tests here: test_org, test_public_repos_url, test_public_repos) ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly checks repo licenses"""
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
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level patching of requests.get"""
        cls.get_patcher = patch("requests.get")

        # Start patcher
        mock_get = cls.get_patcher.start()

        # Configure side_effect so requests.get(url).json() returns the right payload
        def side_effect(url):
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
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos without license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license='apache-2.0'"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)

if __name__ == "__main__":
    unittest.main()
