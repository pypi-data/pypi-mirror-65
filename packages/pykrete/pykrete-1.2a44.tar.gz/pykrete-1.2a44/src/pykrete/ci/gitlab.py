"""
GITLAB CI management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from urllib.parse import urlparse
from gitlab import Gitlab
from pykrete.args import CiIo
from .gitlab_internals.gitlab_upstream_env import GitLabUpstreamEnv
from .gitlab_internals.gitlab_upstream_atrifacts import GitlabUpstreamArtifacts


class GitLab:
    """GitLab CI management"""

    @property
    def _upstream_env(self):
        if not self.__upstream_env:
            self.__upstream_env = GitLabUpstreamEnv(self.__ci_io)
        return self.__upstream_env

    def __init__(self, ci_io=None):
        """Initialize this instance

        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self._logger = logging.getLogger(__name__)
        self.__ci_io = ci_io if ci_io else CiIo()
        self.__gitlab = self._get_gitlab_connection_to_api_url_with_job_token()
        self.__upstream_env = None

    def download_upstream_artifacts(self, target_path=None):
        """Download artifacts from last successful build job in the upstream pipeline

        :param target_path: Target path for downloads
        """
        GitlabUpstreamArtifacts(server=self.__gitlab,
                                project_id=self._upstream_env.project_id,
                                pipeline_id=self._upstream_env.pipeline_id,
                                job_prefix=self._upstream_env.build_job_prefix)\
            .download(target_path)

    def _get_gitlab_connection_to_api_url_with_job_token(self):
        parsed_uri = urlparse(self.__ci_io.read_env('api url'))
        url = f'{parsed_uri.scheme}://{parsed_uri.hostname}/'
        server = Gitlab(url, job_token=self.__ci_io.read_env('job token'))
        self._logger.debug('Attempting connection to %s with the current job token', url)
        server.auth()
        self._logger.debug('Connection to %s succeeded', url)
        return server
