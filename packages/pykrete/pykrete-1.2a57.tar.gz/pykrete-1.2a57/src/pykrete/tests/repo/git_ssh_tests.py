"""
Pykrete repo.Git.git_internals.GitSsh tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

import unittest
import logging
from pykrete.repo.git_internals.git_ssh import GitSsh
from .git_repo_testbed import GitUrlsTestbed, WithTestbed


class PythonGitSshTestCase(unittest.TestCase):
    """E2E tests for pykrete's repo module's git_internals.GitSsh class
    """

    _logger = logging.getLogger(__name__)
    _ssh_file = 'some_file'
    _env = WithTestbed()
    _urls = GitUrlsTestbed()
    _args = 'one', 'two', 'three'

    def test_ssh_set_unset(self):
        """Creation and removal of git ssh connection
        """
        target = self._test_set()
        self._test_unset(target)

    def _test_set(self):
        target = GitSsh(self._setter, self._urls, self._ssh_file, '22')
        self.assertTrue(self._urls.ssh_replaced, 'ssh not replaced on set')
        self.assertTrue(self._env.entered and not self._env.exited, 'wrong env state on set')
        return target

    def _test_unset(self, target):
        target.unset(*self._args)
        self.assertEqual([('http', 'ssh')], self._urls.replaced_urls,
                         'wrong/no URLs replaced on unset')
        self.assertTrue(self._env.entered and self._env.exited, 'wrong env state on unset')
        self.assertEqual(self._args, self._env.args, 'wrong args on unser')

    def _setter(self, **kwargs):
        self._logger.debug('setter called with %s', kwargs)
        cmd = 'GIT_SSH_COMMAND'
        self.assertTrue(cmd in kwargs.keys(), 'SSH command not set')
        self.assertTrue(self._ssh_file in kwargs[cmd], 'file not passed to SSH command')
        self._env.__enter__()
        return self._env


if __name__ == '__main__':
    unittest.main()
