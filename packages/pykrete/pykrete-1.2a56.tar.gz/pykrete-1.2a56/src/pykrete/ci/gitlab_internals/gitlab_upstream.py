"""
GITLAB CI upstream management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from gitlab import Gitlab
from pykrete.args import CiIo
from .gitlab_upstream_env import GitLabUpstreamEnv
from .gitlab_upstream_atrifacts import GitlabUpstreamArtifacts


class GitLabUpstream:
    """GitLab CI upstream management"""

    @property
    def artifacts(self):
        """
        :return: Upstream artifacts
        """
        if not self._artifacts:
            self._artifacts = GitlabUpstreamArtifacts(
                server=self.__gitlab,
                upstream_env=self.__upstream_env)
        return self._artifacts

    def __init__(self, url, ci_io=None):
        """Initialize this instance

        :param url: gitlab URL
        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self._logger = logging.getLogger(__name__)
        self.__ci_io = ci_io if ci_io else CiIo()
        self.__upstream_env = GitLabUpstreamEnv()
        self.__gitlab = self._get_gitlab_connection_with_upstream_key_to_api_url(url)
        self._artifacts = None

    def _get_gitlab_connection_with_upstream_key_to_api_url(self, url):
        server = Gitlab(url, private_token=self.__upstream_env.key)
        self._logger.debug('Attempting connection to %s with the upstream token', url)
        server.auth()
        self._logger.debug('Connection to %s succeeded', url)
        return server
