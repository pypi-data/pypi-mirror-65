"""
GITLAB CI management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from urllib.parse import urlparse
from pykrete.args import CiIo
from .gitlab_internals.gitlab_upstream import GitLabUpstream


class GitLab:
    """GitLab CI management"""

    @property
    def upstream(self):
        """
        :return: upstream CI management
        """
        if not self._upstream:
            self._upstream = GitLabUpstream(self._get_gitlab_api_url(), self.__ci_io)
        return self._upstream

    def __init__(self, ci_io=None):
        """Initialize this instance

        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self._logger = logging.getLogger(__name__)
        self.__ci_io = ci_io if ci_io else CiIo()
        self._upstream = None

    def _get_gitlab_api_url(self):
        parsed_uri = urlparse(self.__ci_io.read_env('api url'))
        url = f'{parsed_uri.scheme}://{parsed_uri.hostname}/'
        return url
