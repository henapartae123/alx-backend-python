#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
# from fixtures import (
#     org_payload,
#     repos_payload,
#     expected_repos,
#     apache2_repos
# )


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns value from get_json."""
        test_instance = GithubOrgClient(org_name)
        test_instance.org  # trigger property access

        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the mocked repos_url."""
        client = GithubOrgClient("test")
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns repo names and calls get_json."""
        # Mocked payload for get_json
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        # Create a client
        client = GithubOrgClient("test")

        # Mock _public_repos_url property to return a dummy URL
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(sorted(result), expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url.return_value)
    # @parameterized.expand([
    #     ({"license": {"key": "my_license"}}, "my_license", True),
    #     ({"license": {"key": "other_license"}}, "my_license", False),
    # ])
#     def test_has_license(self, repo, license_key, expected):
#         """Test that has_license returns True/False depending on license key."""
#         self.assertEqual(
#             GithubOrgClient.has_license(repo, license_key), expected
#         )

# @parameterized_class(
#     ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
#     [(org_payload, repos_payload, expected_repos, apache2_repos)],
# )
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration tests for GithubOrgClient.public_repos."""

#     @classmethod
#     def setUpClass(cls):
#         """Start patching client.get_json for integration tests."""
#         cls.get_patcher = patch("client.get_json")
#         cls.mock_get_json = cls.get_patcher.start()

#         def get_json_side_effect(url):
#             if url.endswith("/repos"):
#                 return cls.repos_payload
#             return cls.org_payload

#         cls.mock_get_json.side_effect = get_json_side_effect

#     @classmethod
#     def tearDownClass(cls):
#         """Stop patching."""
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Integration test for public_repos returns expected repo names."""
#         client = GithubOrgClient("test")
#         self.assertEqual(
#             sorted(client.public_repos()),
#             sorted(self.expected_repos)
#         )

#     def test_public_repos_with_license(self):
#         """Integration test for filtering by license."""
#         client = GithubOrgClient("test")
#         self.assertEqual(
#             sorted(client.public_repos("apache-2.0")),
#             sorted(self.apache2_repos)
#         )


if __name__ == "__main__":
    unittest.main()
