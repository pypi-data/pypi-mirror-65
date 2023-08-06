"""
GIT repository push management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from git import GitCommandError
from pykrete.credentials import SshTarget
from .git_urls import GitUrls
from .git_ssh import GitSsh


class GitPush(SshTarget):
    """Handles pushing to a git repo"""

    def __init__(self, repo, credentials=None, remote='origin'):
        """Initialize this repository

        :param repo: git repository
        :param credentials: git credential (optional, defaults to None)
        """
        self._logger = logging.getLogger(__name__)
        self._repo = repo
        self._credentials = credentials
        self._remote = repo.remotes[remote]
        self._urls = GitUrls(self._remote)
        self._active_credentials = None

    def __enter__(self):
        if self._credentials:
            self.accept(self._credentials)
        return self

    def __exit__(self, *args):
        if self._active_credentials:
            self._active_credentials.unset(*args)

    def push(self, item):
        """Push the item

        :param item: item to push
        """
        try:
            self._logger.debug('Pushing %s', item)
            self._remote.push(item)
            self._logger.debug('%s pushed', item)
        except GitCommandError as exc:
            self._logger.error('Push failed: %s', exc)
            raise

    def set_ssh(self, private_key_file_path, ssh_port):
        """Set SSH private key to the specified path

        :param private_key_file_path: Path to private key file
        :param ssh_port: SSH port
        """
        self._active_credentials = GitSsh(
            self._repo.git.custom_environment, self._urls, private_key_file_path, ssh_port)
