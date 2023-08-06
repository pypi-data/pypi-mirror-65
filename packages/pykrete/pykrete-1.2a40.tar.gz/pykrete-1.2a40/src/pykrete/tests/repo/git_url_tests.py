"""
Pykrete repo.Git.git_internals.GitUrl tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
from pykrete.repo.git_internals.git_urls import GitUrls
from .git_repo_testbed import GitRepoRemoteTestbed


class PythonGitUrlsTestCase(unittest.TestCase):
    """E2E tests for pykrete's repo module's git_internals.GitUrl class
    """

    def test_no_configured_ssh_urls(self):
        """Verifies no ssh urls returned when none were configured
        """
        target = GitUrls(GitRepoRemoteTestbed(['http://google.com/my.git',
                                               'https://example.org/project/his.git']))
        self.assertFalse(target.configured_ssh_urls, 'got ssh urls even though there were none')

    def test_some_configured_ssh_urls(self):
        """Verifies ssh urls returned when configured
        """
        expected_url = 'ssh://git@google.com:my.git'
        target = GitUrls(GitRepoRemoteTestbed(['http://google.com/my.git', expected_url]))
        self.assertEqual([expected_url], target.configured_ssh_urls, 'wrong/no URL returned')

    def test_configure_ssh_url_and_save_original_http(self):
        """Verifies correct replacement of http URL with SSH URL
        """
        self._test_configure_ssh_url_and_save_original(
            'http://google.com/project/my.git', '22',
            'ssh://git@google.com/project/my.git')

    def test_configure_ssh_url_and_save_original_https(self):
        """Verifies correct replacement of https URL with SSH URL
        """
        self._test_configure_ssh_url_and_save_original(
            'https://example.org/project/his.git', '22',
            'ssh://git@example.org/project/his.git')

    def test_configure_ssh_url_and_save_original_https_with_token(self):
        """Verifies correct replacement of tokenized https URL with SSH URL
        """
        self._test_configure_ssh_url_and_save_original(
            'https://gitlab-ci-token:[MASKED]'
            '@gitlab.devtools.intel.com/ait-projects/testing-grounds.git', '1234',
            'ssh://git@gitlab.devtools.intel.com:1234/ait-projects/testing-grounds.git')

    def test_configure_ssh_url_and_save_original_with_no_urls(self):
        """Verifies correct replacement of http URL with SSH URL
        """
        target = GitUrls(GitRepoRemoteTestbed([]))
        with self.assertRaises(IOError):
            target.configure_ssh_url_and_save_original('22')

    def _test_configure_ssh_url_and_save_original(self, original_url, port, expected_url):
        """Verifies correct replacement of http* URL with SSH URL
        """
        remote = GitRepoRemoteTestbed([original_url])
        target = GitUrls(remote)
        self.assertEqual([], target.configured_ssh_urls, 'ssh url returned before being configured')
        set_urls = target.configure_ssh_url_and_save_original(port)
        self.assertEqual((original_url, expected_url), set_urls, 'wrong history returned')
        self.assertEqual([(expected_url, original_url)], remote.urls_set, 'wrong url set')
        self.assertEqual([expected_url], target.configured_ssh_urls, 'wrong ssh url returned')


if __name__ == '__main__':
    unittest.main()
