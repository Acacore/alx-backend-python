#!/usr/bin/env python3
"""A github org client
"""
from typing import (
    List,
    Dict,
)

from utils import (
    get_json,
    access_nested_map,
    memoize,
)

'''The class fetches an org’s info from GitHub, fetches all its repos, and can list them — either all repos or only those with a specific license.'''
class GithubOrgClient:
    """A Githib org client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    # Initialization
    def __init__(self, org_name: str) -> None:
        """Init method of GithubOrgClient"""
        self._org_name = org_name

    
    '''
        Getting organization info
        This fetches the JSON dictionary for the organization (things like name, ID, repos_url, etc.)
        Thanks to @memoize, if you call client.org again, it won’t fetch the URL again — it will reuse the cached value
    '''
    @memoize
    def org(self) -> Dict:
        """Memoize org"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    '''
    Looks into the org dictionary, pulls out the "repos_url" field.
    That’s the link where GitHub lists all public repos of that org.
    ''' 
    @property
    def _public_repos_url(self) -> str:
        """Public repos URL"""
        return self.org["repos_url"]


    '''
    Calls get_json on the repos URL.

That fetches a list of dictionaries, where each dictionary describes one repo (name, description, license, etc.).

Again, @memoize caches it.'''
    @memoize
    def repos_payload(self) -> Dict:
        """Memoize repos payload"""
        return get_json(self._public_repos_url)
    
    '''Loops over all repos in the payload.

For each repo, it extracts the "name".

If you pass a license filter:

Calls has_license(repo, license) to check if that repo has the given license.

Keeps only repos that match.

So you either get all repo names, or only repo names with a specific license.'''

    def public_repos(self, license: str = None) -> List[str]:
        """Public repos"""
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Static: has_license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license